from django.urls import path
from ddd.order_management.presentation import webhook_apis

urlpatterns = [
    path('<str:tenant_id>/tenant_add_order', webhook_apis.tenant_add_order_api, name='tenant_webhook_tenant_add_order_sync'),
    path('shipping_updates', webhook_apis.shipment_updates_api, name='shipment_updates_api_sync'),
]