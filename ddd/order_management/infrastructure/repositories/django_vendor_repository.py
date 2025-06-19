import pytz, uuid
from datetime import datetime
from typing import List
from ddd.order_management.domain import repositories, enums, value_objects, exceptions, models
from order_management import models as django_snapshots
from ddd.order_management.infrastructure import django_mappers

class DjangoVendorRepositoryImpl(repositories.VendorAbstract):

    def get_line_items(self, vendor_id: str, skus: List[str]) -> models.LineItem:
        try:
            django_vendor_details = django_snapshots.VendorDetailsSnapshot.objects.get(
                vendor_id=vendor_id, 
                is_active=True
            )
        except django_snapshots.VendorDetailsSnapshot.DoesNotExist:
            raise exceptions.VendorDetailsException(f"Vendor {vendor_id} Details not available")

        django_products = django_snapshots.VendorProductSnapshot.objects.filter(
            vendor_id=vendor_id, 
            product_sku__in=skus,
            is_active=True
        )

        if not django_products.exists():
            raise exceptions.VendorProductNotFoundException(f"Vendor {vendor_id} Products {','.join(skus)} not available")

        line_items = []
        for product in django_products:

            #do this to fit w LineItemMapper expected fields
            product.order_quantity = product.stock
            product.vendor_name = django_vendor_details.name
            product.vendor_country = django_vendor_details.country
            product.is_free_gift = False
            product.is_taxable = True

            line_items.append(
                django_mappers.LineItemMapper.to_domain(product)
            )

        return line_items


    def get_offers(self, vendor_id: str) -> List[value_objects.OfferStrategy]:
        offers = django_snapshots.VendorOfferSnapshot.objects.filter(vendor_id=vendor_id, is_active=True).prefetch_related("coupon").values()
        offer_list = [
            { **offer, "coupons": list(django_snapshots.VendorCouponSnapshot.objects.filter(offer_id=offer.get("offer_id")).values()) }
            for offer in offers
        ]

        final_offers = []
        for offer in offer_list:
            try:
                final_offers.append(django_mappers.OfferStrategyMapper.to_domain(offer))
            except exceptions.OfferStrategyException as e:
                #TODO send notification for invalid offer?
                print(f"DjangoVendorRepository.get_offer exception > {str(e)}")
                continue
        return final_offers


    def get_shipping_options(self, vendor_id: uuid.UUID) -> List[value_objects.ShippingOptionStrategy]:
        shipping_options = django_snapshots.VendorShippingOptionSnapshot.objects.filter(vendor_id=vendor_id, is_active=True)
        final_opts = []
        for option in shipping_options.values():
            option.pop("id")
            try:
                final_opts.append(django_mappers.ShippingOptionStrategyMapper.to_domain(option))
            except (ValueError) as e:
                print(f"DjangoVendorRepository.get_shipping_options exception > {str(e)}")
                continue
        return final_opts
