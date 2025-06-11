from ddd.order_management.infrastructure import snapshot_services, adapters

def run_vendor_offer_snapshot_sync():
    provider = adapters.FakeVendorOfferSnapshotAdapter()
    django_vendor_offer_snapshot = snapshot_services.DjangoVendorOfferSnapshotSyncService(provider)
    django_vendor_offer_snapshot.sync()

def run_vendor_product_snapshot_sync():
    provider = adapters.FakeVendorProductSnapshotAdapter()
    django_vendor_offer_snapshot = snapshot_services.DjangoVendorProductSnapshotSyncService(provider)
    django_vendor_offer_snapshot.sync()