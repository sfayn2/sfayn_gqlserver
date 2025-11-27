from django.urls import path
from ddd.order_management.presentation import webhook_apis

urlpatterns = [
    path('webhook/add_order/<str:tenant_id>', webhook_apis.tenant_add_order_api, name='tenant_webhook_tenant_add_order_sync'),
    path('webhook/shipping_updates/<str:saas_id>', webhook_apis.shipment_updates_api, name='shipment_updates_api_sync'),
]