from __future__ import annotations
import pytz, uuid
from datetime import datetime
from typing import List
from ddd.order_management.domain import repositories, enums, value_objects, exceptions, models
from order_management import models as django_snapshots
from ddd.order_management.infrastructure import django_mappers

class DjangoVendorRepositoryImpl(repositories.VendorAbstract):

    def get_line_items(
        self, vendor_id: str, product_skus_input: List[ProductSkuDTO]
    ) -> List[models.LineItem]:
        vendor_details = self._get_active_vendor_details(vendor_id)

        product_sku_map = {sku.product_sku: sku.order_quantity for sku in product_skus_input}

        available_products = list(django_snapshots.VendorProductSnapshot.objects.filter(
                vendor_id=vendor_id, 
                product_sku__in=product_sku_map.keys(),
                is_active=True
            )
        )

        if not available_products:
            raise exceptions.VendorProductNotFoundException(
                f"Vendor {vendor_id} does not offer products: { ','.join(product_sku_map.keys()) } not available"
            )

        line_items = []
        for snapshot in available_products:
            #do this to fit w LineItemMapper expected fields
            snapshot.order_quantity = product_sku_map.get(snapshot.product_sku)
            snapshot.vendor_name = vendor_details.name
            snapshot.vendor_country = vendor_details.country
            snapshot.is_free_gift = False
            snapshot.is_taxable = True

            line_items.append(
                django_mappers.LineItemMapper.to_domain(snapshot)
            )

        return line_items


    def get_offers(
        self, vendor_id: str
    ) -> List[value_objects.OfferStrategy]:
        offers = django_snapshots.VendorOfferSnapshot.objects.filter(vendor_id=vendor_id, is_active=True).values()
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


    def get_shipping_options(
        self, vendor_id: uuid.UUID
    ) -> List[value_objects.ShippingOptionStrategy]:
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

    def _get_active_vendor_details(self, vendor_id: str):
        try:
            return django_snapshots.VendorDetailsSnapshot.objects.get(
                vendor_id=vendor_id, 
                is_active=True
            )
        except django_snapshots.VendorDetailsSnapshot.DoesNotExist:
            raise exceptions.VendorDetailsException(
                f"Vendor details not found for vendor_id={vendor_id}"
            )

