from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Order, OrderItem, Service, UserProfile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name"]


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = UserProfile
        fields = ["id", "user", "phone", "company", "position", "created_at"]


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = [
            "id",
            "name",
            "description",
            "price",
            "status",
            "image_key",
            "video_key",
            "image_key_2",
            "image_key_3",
            "image_key_4",
            "image_key_5",
            "category",
            "manufacturer",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["created_at", "updated_at"]


class OrderItemSerializer(serializers.ModelSerializer):
    service = ServiceSerializer(read_only=True)
    service_id = serializers.IntegerField(write_only=True)
    subtotal = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = OrderItem
        fields = ["id", "order", "service", "service_id", "quantity", "position", "is_main", "subtotal"]
        read_only_fields = ["order", "subtotal"]


class OrderSerializer(serializers.ModelSerializer):
    creator = UserSerializer(read_only=True)
    items = OrderItemSerializer(source="orderitem_set", many=True, read_only=True)
    status_display = serializers.CharField(source="get_status_display", read_only=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "status",
            "status_display",
            "creator",
            "created_at",
            "formed_at",
            "completed_at",
            "moderator",
            "total",
            "items_count",
            "comment",
            "items",
        ]
        read_only_fields = ["creator", "total", "items_count", "created_at"]
