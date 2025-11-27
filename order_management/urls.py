from django.urls import path
from ddd.order_management.presentation import webhook_apis

urlpatterns = [
    path('webhook/add-order/<str:tenant_id>', webhook_apis.add_order_webhook, name='add_order_webhook'),
    path('webhook/shipment-tracker/<str:saas_id>', webhook_apis.shipment_tracker_webhook, name='shipment_tracker_webhook'),
]