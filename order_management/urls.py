from django.urls import path
from ddd.order_management.presentation import webhook_apis

urlpatterns = [
    path('<str:provider>/<str:tenant_id>/product_update', webhook_apis.product_update_api, name='tenant_webhook_product_sync'),
]