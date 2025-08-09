from django.urls import path
from ddd.order_management.presentation import webhook_apis

urlpatterns = [
    path('<str:provider>/<str:tenant_id>/product_sync', webhook_apis.product_sync, 'tenant_webhook_product_sync'),
]