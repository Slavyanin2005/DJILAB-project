from django.db.models import Max
from django.shortcuts import get_object_or_404
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .models import Order, OrderItem, Service, UserProfile
from .serializers import OrderSerializer, ServiceSerializer, UserProfileSerializer


class ServiceViewSet(viewsets.ModelViewSet):
    """API для услуг/товаров"""

    queryset = Service.objects.filter(status="active")
    serializer_class = ServiceSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name", "description", "category"]
    ordering_fields = ["price", "name", "created_at"]
    permission_classes = [AllowAny]

    @action(detail=True, methods=["post"])
    def add_to_order(self, request, pk=None):
        """Добавить услугу в заказ"""
        service = self.get_object()
        quantity = request.data.get("quantity", 1)

        order = Order.objects.filter(
            creator=request.user if request.user.is_authenticated else None, status="draft"
        ).first()

        if not order:
            max_id = Order.objects.aggregate(Max("id"))["id__max"] or 0
            order = Order.objects.create(
                id=max_id + 1,
                status="draft",
                creator=request.user if request.user.is_authenticated else None,
            )

        order_item, created = OrderItem.objects.get_or_create(
            order=order, service=service, defaults={"quantity": quantity}
        )

        if not created:
            order_item.quantity += quantity
            order_item.save()

        order.items_count = OrderItem.objects.filter(order=order).count()
        order.total = sum(item.subtotal for item in OrderItem.objects.filter(order=order))
        order.save()

        return Response(OrderSerializer(order).data, status=status.HTTP_200_OK)


class OrderViewSet(viewsets.ModelViewSet):
    """API для заказов"""

    serializer_class = OrderSerializer
    # Разрешаем все действия для лабораторной (в продакшене — только IsAuthenticated)
    permission_classes = [AllowAny]

    def get_queryset(self):
        # Возвращаем все заказы, кроме удалённых
        return Order.objects.exclude(status="deleted").order_by("-created_at")

    def create(self, request, *args, **kwargs):
        """Создать новый заказ-черновик с авто-генерацией ID"""
        max_id = Order.objects.aggregate(Max("id"))["id__max"] or 0
        order = Order.objects.create(
            id=max_id + 1,
            status="draft",
            creator=request.user if request.user.is_authenticated else None,
            total=0,
            items_count=0,
        )
        serializer = self.get_serializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def _check_draft_permission(self, order):
        """Проверка: можно ли изменять этот заказ"""
        if order.status != "draft":
            return False, "Нельзя изменить завершённый заказ"
        return True, None

    @action(detail=True, methods=["post"])
    def add_item(self, request, pk=None):
        """Добавить позицию в заказ"""
        order = self.get_object()

        allowed, error = self._check_draft_permission(order)
        if not allowed:
            return Response({"error": error}, status=status.HTTP_400_BAD_REQUEST)

        service_id = request.data.get("service_id")
        quantity = request.data.get("quantity", 1)

        service = get_object_or_404(Service, id=service_id, status="active")

        order_item, created = OrderItem.objects.get_or_create(
            order=order, service=service, defaults={"quantity": quantity}
        )

        if not created:
            order_item.quantity += quantity
            order_item.save()

        order.items_count = OrderItem.objects.filter(order=order).count()
        order.total = sum(item.subtotal for item in OrderItem.objects.filter(order=order))
        order.save()

        return Response(OrderSerializer(order).data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"])
    def update_item(self, request, pk=None):
        """Изменить количество позиции в заказе"""
        order = self.get_object()

        allowed, error = self._check_draft_permission(order)
        if not allowed:
            return Response({"error": error}, status=status.HTTP_400_BAD_REQUEST)

        item_id = request.data.get("item_id")
        action = request.data.get("action")

        order_item = get_object_or_404(OrderItem, id=item_id, order=order)

        if action == "increase":
            order_item.quantity += 1
        elif action == "decrease":
            if order_item.quantity > 1:
                order_item.quantity -= 1
            else:
                order_item.delete()
                order.items_count = OrderItem.objects.filter(order=order).count()
                order.total = sum(item.subtotal for item in OrderItem.objects.filter(order=order))
                order.save()
                return Response(OrderSerializer(order).data, status=status.HTTP_200_OK)

        order_item.save()

        order.items_count = OrderItem.objects.filter(order=order).count()
        order.total = sum(item.subtotal for item in OrderItem.objects.filter(order=order))
        order.save()

        return Response(OrderSerializer(order).data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"])
    def remove_item(self, request, pk=None):
        """Удалить позицию из заказа"""
        order = self.get_object()

        allowed, error = self._check_draft_permission(order)
        if not allowed:
            return Response({"error": error}, status=status.HTTP_400_BAD_REQUEST)

        item_id = request.data.get("item_id")
        OrderItem.objects.filter(id=item_id, order=order).delete()

        order.items_count = OrderItem.objects.filter(order=order).count()
        order.total = sum(item.subtotal for item in OrderItem.objects.filter(order=order))
        order.save()

        return Response(OrderSerializer(order).data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"])
    def submit(self, request, pk=None):
        """Отправить заказ"""
        order = self.get_object()

        allowed, error = self._check_draft_permission(order)
        if not allowed:
            return Response({"error": error}, status=status.HTTP_400_BAD_REQUEST)

        order.status = "formed"
        order.save()

        return Response(OrderSerializer(order).data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"])
    def delete(self, request, pk=None):
        """Логическое удаление заказа"""
        order = self.get_object()

        if order.status != "draft":
            return Response({"error": "Можно удалить только черновик"}, status=status.HTTP_400_BAD_REQUEST)

        order.status = "deleted"
        order.save()

        return Response(OrderSerializer(order).data, status=status.HTTP_200_OK)


class UserProfileViewSet(viewsets.ModelViewSet):
    """API для профилей пользователей"""

    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return UserProfile.objects.filter(user=self.request.user)
        return UserProfile.objects.none()
