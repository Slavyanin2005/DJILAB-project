from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.db import connection, transaction
from django.db.models import Max
from django.shortcuts import get_object_or_404, redirect, render

from .models import Order, OrderItem, Service


def services_view(request):

    # GET services контроллер списка услуг с фильтрацией и поиском
    search_query = request.GET.get("search", "")
    services = Service.objects.filter(status="active")

    if search_query:
        services = services.filter(name__icontains=search_query)

    # черновик текущего пользователя
    draft_order = None
    if request.user.is_authenticated:
        draft_order = Order.objects.filter(creator=request.user, status="draft").first()

    cart_count = draft_order.items_count if draft_order else 0
    draft_order_id = draft_order.id if draft_order else None

    context = {
        "services": services,
        "search_query": search_query,
        "cart_count": cart_count,
        "draft_order_id": draft_order_id,
        "MEDIA_URL": settings.MEDIA_URL,
    }
    return render(request, "index.html", context)


def service_detail_view(request, service_id):

    # GET services/{id}/ Контроллер детальной информации об услуге

    service = get_object_or_404(Service, id=service_id, status="active")

    # черновик текущего пользователя
    draft_order = None
    if request.user.is_authenticated:
        draft_order = Order.objects.filter(creator=request.user, status="draft").first()

    cart_count = draft_order.items_count if draft_order else 0
    draft_order_id = draft_order.id if draft_order else None

    context = {
        "service": service,
        "cart_count": cart_count,
        "draft_order_id": draft_order_id,
        "MEDIA_URL": settings.MEDIA_URL,
    }
    return render(request, "product.html", context)


def order_view(request, order_id):
    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        draft_order = (
            Order.objects.filter(creator=request.user, status="draft").first()
            if request.user.is_authenticated
            else None
        )

        return render(
            request,
            "cart.html",
            {
                "no_order": True,
                "cart_count": draft_order.items_count if draft_order else 0,
                "draft_order_id": draft_order.id if draft_order else None,
                "MEDIA_URL": settings.MEDIA_URL,
            },
        )

    if order.status == "deleted":
        return redirect("services")

    if request.user.is_authenticated and order.creator != request.user:
        return redirect("services")

    is_readonly = order.status != "draft"

    order_items = OrderItem.objects.filter(order=order).select_related("service")

    context = {
        "order": order,
        "order_items": order_items,
        "cart_count": order.items_count,
        "draft_order_id": order.id if order.status == "draft" else None,
        "is_readonly": is_readonly,
        "MEDIA_URL": settings.MEDIA_URL,
    }
    return render(request, "cart.html", context)


@login_required
@transaction.atomic
def add_to_order_view(request, order_id):

    # POST orders{id} add добавление услуги в заявку через ORM

    if request.method == "POST":
        service_id = request.POST.get("service_id")
        quantity = int(request.POST.get("quantity", 1))

        service = get_object_or_404(Service, id=service_id, status="active")

        # Поиск существующего черновика юзера
        order = Order.objects.filter(creator=request.user, status="draft").first()

        # Если нет черновика то создаем заявку
        if not order:
            max_id = Order.objects.aggregate(Max("id"))["id__max"] or 0
            order = Order.objects.create(
                id=max_id + 1,
                status="draft",
                creator=request.user,
                total=0,
                items_count=0,
            )

        # Добавляем позиции
        order_item, created = OrderItem.objects.get_or_create(
            order=order,
            service=service,
            defaults={
                "quantity": quantity,
                "position": OrderItem.objects.filter(order=order).count(),
            },
        )

        # Если позиция уже есть то увеличиваем количество
        if not created:
            order_item.quantity += quantity
            order_item.save()

        # Пересчет
        order.items_count = OrderItem.objects.filter(order=order).count()
        order.total = sum(item.subtotal for item in OrderItem.objects.filter(order=order))
        order.save()

        return redirect("order", order_id=order.id)

    return redirect("services")


@login_required
@transaction.atomic
def update_quantity_view(request, order_id, item_id):

    # POST orders/id} update{item_id} зменить количество позиции через ORM

    if request.method == "POST":
        order = get_object_or_404(Order, id=order_id)

        if order.creator != request.user or order.status != "draft":
            return redirect("services")

        action = request.POST.get("action")
        order_item = get_object_or_404(OrderItem, id=item_id, order=order)

        if action == "increase":
            order_item.quantity += 1
        elif action == "decrease":
            if order_item.quantity > 1:
                order_item.quantity -= 1
            else:
                return redirect("remove_from_order", order_id=order.id, item_id=item_id)

        order_item.save()

        # Пересчитываем total и items_count
        order.items_count = OrderItem.objects.filter(order=order).count()
        order.total = sum(item.subtotal for item in OrderItem.objects.filter(order=order))
        order.save()

        return redirect("order", order_id=order.id)

    return redirect("services")


@login_required
@transaction.atomic
def remove_from_order_view(request, order_id, item_id):
    """
    POST /orders/{id}/remove/{item_id}/
    Удалить позицию из заявки через ORM
    """
    if request.method == "POST":
        order = get_object_or_404(Order, id=order_id)

        if order.creator != request.user or order.status != "draft":
            return redirect("services")

        OrderItem.objects.filter(id=item_id, order=order).delete()

        # Пересчитываем total и items_count
        order.items_count = OrderItem.objects.filter(order=order).count()
        order.total = sum(item.subtotal for item in OrderItem.objects.filter(order=order))
        order.save()

        return redirect("order", order_id=order.id)

    return redirect("services")


@login_required
def delete_order_view(request, order_id):
    # POST orders{id}delete логическое удаление заявки через SQL UPDATE
    if request.method == "POST":
        order = get_object_or_404(Order, id=order_id)

        if order.creator != request.user:
            return redirect("services")

        with connection.cursor() as cursor:
            cursor.execute("UPDATE orders SET status = %s WHERE id = %s", ["deleted", order_id])

        return redirect("services")

    return redirect("services")


@login_required
def orders_history_view(request):

    # GET ordershistory страница истории заявок текущего пользователя

    user_orders = Order.objects.filter(creator=request.user).order_by("-created_at")

    draft_order = Order.objects.filter(creator=request.user, status="draft").first()

    cart_count = draft_order.items_count if draft_order else 0

    context = {
        "user_orders": user_orders,
        "cart_count": cart_count,
        "draft_order_id": draft_order.id if draft_order else None,
        "MEDIA_URL": settings.MEDIA_URL,
    }
    return render(request, "orders_history.html", context)
