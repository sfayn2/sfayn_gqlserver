
class OrderFulfillment:

    def fulfill_order(self, fulfillment_service: None ):
        fulfill_by_address = {} #fulfill by shipping address
        for item in self.get_order_fulfillments():
            if item.shipping_address not in fulfill_by_address.items():
                fulfill_by_address[item.shipping_address] = []
            fulfill_by_address[item.shipping_address].append(item)

        for item in fulfill_by_address.items():