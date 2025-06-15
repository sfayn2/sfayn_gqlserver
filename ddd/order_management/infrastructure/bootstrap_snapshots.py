from ddd.order_management.infrastructure import snapshot_services

SYNC_TASKS = [
    (
        snapshot_services.DjangoVendorDetailsSnapshotSyncService
        snapshot_services.FakeVendorDetailsSnapshotProvider,


    )
]

def run_vendor_details_snapshot_sync():
    provider = snapshot_services.FakeVendorDetailsSnapshotProvider()
    django_vendor_details_snapshot = snapshot_services.DjangoVendorDetailsSnapshotSyncService(provider)
    django_vendor_details_snapshot.sync()
    
    print("Vendor details synced.")

def run_vendor_offer_snapshot_sync():
    provider = snapshot_services.FakeVendorOfferSnapshotProvider()
    django_vendor_offer_snapshot = snapshot_services.DjangoVendorOfferSnapshotSyncService(provider)
    django_vendor_offer_snapshot.sync()
    
    print("Vendor offer snapshot synced.")

def run_vendor_product_snapshot_sync():
    provider = snapshot_services.FakeVendorProductSnapshotProvider()
    django_vendor_offer_snapshot = snapshot_services.DjangoVendorProductSnapshotSyncService(provider)
    django_vendor_offer_snapshot.sync()

    print("Vendor product snapshot synced.")

def run_vendor_shippingoptions_snapshot_sync():
    provider = snapshot_services.FakeVendorShippingOptionSnapshotProvider()
    django_vendor_shippingoptions_snapshot = snapshot_services.DjangoVendorShippingOptionSnapshotSyncService(provider)
    django_vendor_shippingoptions_snapshot.sync()

    print("Vendor shipping options snapshot synced.")

def run_customer_snapshot_sync():
    provider = snapshot_services.FakeCustomerSnapshotProvider()
    django_customer_snapshot = snapshot_services.DjangoCustomerSnapshotSyncService(provider)
    django_customer_snapshot.sync()

    print("Customer snapshot synced.")

def run_user_auth_snapshot_sync():
    provider = snapshot_services.DjangoUserAuthorizationSnapshotProvider()
    django_user_auth = snapshot_services.DjangoUserAuthorizationSnapshotSyncService(provider)
    django_user_auth.sync()

    print("User Auth snapshot synced.")

def run_all_snapshot_sync():
    run_vendor_details_snapshot_sync()
    run_vendor_offer_snapshot_sync()
    run_vendor_product_snapshot_sync()
    run_vendor_shippingoptions_snapshot_sync()
    run_customer_snapshot_sync()
    run_user_auth_snapshot_sync()