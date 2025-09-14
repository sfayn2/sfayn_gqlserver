from django.urls import path
from ddd.order_management.presentation import webhook_apis

urlpatterns = [
    path('<str:provider>/<str:tenant_id>/tenant_workflow_update', webhook_apis.tenant_workflow_update_api, name='tenant_webhook_tenant_workflow_sync'),
    path('<str:provider>/<str:tenant_id>/tenant_rolemap_update', webhook_apis.tenant_rolemap_update_api, name='tenant_webhook_tenant_rolemap_sync'),
    path('<str:provider>/<str:tenant_id>/tenant_create_order', webhook_apis.tenant_create_order_api, name='tenant_webhook_tenant_create_order_sync'),
]