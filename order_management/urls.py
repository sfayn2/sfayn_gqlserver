from django.urls import path
from ddd.order_management.presentation import webhook_apis

urlpatterns = [
    path('<str:tenant_id>/tenant_create_order', webhook_apis.tenant_create_order_api, name='tenant_webhook_tenant_create_order_sync'),
]