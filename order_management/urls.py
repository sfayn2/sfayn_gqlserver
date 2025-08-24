from django.urls import path
from ddd.order_management.presentation import webhook_apis

urlpatterns = [
    path('<str:provider>/<str:tenant_id>/product_update', webhook_apis.product_update_api, name='tenant_webhook_product_sync'),
    path('<str:provider>/<str:tenant_id>/vendor_details_update', webhook_apis.vendor_details_update_api, name='tenant_webhook_vendor_details_sync'),
    path('<str:provider>/<str:tenant_id>/vendor_coupon_update', webhook_apis.vendor_coupon_update_api, name='tenant_webhook_vendor_coupon_sync'),
    path('<str:provider>/<str:tenant_id>/vendor_offer_update', webhook_apis.vendor_offer_update_api, name='tenant_webhook_vendor_offer_sync'),
    path('<str:provider>/<str:tenant_id>/vendor_shippingoption_update', webhook_apis.vendor_shippingoption_update_api, name='tenant_webhook_vendor_shippingoption_sync'),
    path('<str:provider>/<str:tenant_id>/vendor_paymentoption_update', webhook_apis.vendor_paymentoption_update_api, name='tenant_webhook_vendor_paymentoption_sync'),
    path('<str:provider>/<str:tenant_id>/vendor_taxoption_update', webhook_apis.vendor_taxoption_update_api, name='tenant_webhook_vendor_taxoption_sync'),
]