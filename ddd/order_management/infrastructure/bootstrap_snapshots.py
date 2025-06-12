from ddd.order_management.infrastructure import snapshot_services

def run_vendor_offer_snapshot_sync():
    provider = snapshot_services.FakeVendorOfferSnapshotProvider()
    django_vendor_offer_snapshot = snapshot_services.DjangoVendorOfferSnapshotSyncService(provider)
    django_vendor_offer_snapshot.sync()

def run_vendor_product_snapshot_sync():
    provider = snapshot_services.FakeVendorProductSnapshotProvider()
    django_vendor_offer_snapshot = snapshot_services.DjangoVendorProductSnapshotSyncService(provider)
    django_vendor_offer_snapshot.sync()

def run_vendor_shippingoptions_snapshot_sync():
    provider = snapshot_services.FakeVendorShippingOptionSnapshotProvider()
    django_vendor_shippingoptions_snapshot = snapshot_services.DjangoVendorShippingOptionSnapshotSyncService(provider)
    django_vendor_shippingoptions_snapshot.sync()