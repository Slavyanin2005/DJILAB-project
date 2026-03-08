from django.urls import path

from . import views

urlpatterns = [
    path("", views.services_view, name="services"),
    path("services/<int:service_id>/", views.service_detail_view, name="service_detail"),
    path("orders/<int:order_id>/", views.order_view, name="order"),
    path("orders/history/", views.orders_history_view, name="orders_history"),
    path("orders/<int:order_id>/add/", views.add_to_order_view, name="add_to_order"),
    path("orders/<int:order_id>/update/<int:item_id>/", views.update_quantity_view, name="update_quantity"),
    path("orders/<int:order_id>/remove/<int:item_id>/", views.remove_from_order_view, name="remove_from_order"),
    path("orders/<int:order_id>/delete/", views.delete_order_view, name="delete_order"),
]
