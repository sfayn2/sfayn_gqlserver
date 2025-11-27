from django.urls import path
from ddd.order_management.presentation import webhook_apis

urlpatterns = [
    path('webhook/add-order/<str:tenant_id>', webhook_apis.add_order_webhook, name='add_order_webhook'),

    # default shipment tracker webhook provider
    path('webhook/shipment-tracker/<str:saas_id>', webhook_apis.shipment_tracker_webhook, name='shipment_tracker_webhook'),

    # if tenant decided to have their own shipment tracker webhook provider
    path('webhook/shipment-tracker-tenant/<str:tenant_id>', webhook_apis.shipment_tracker_webhook_tenant, name='shipment_tracker_webhook_tenant'),
]