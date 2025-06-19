from ddd.order_management.domain import repositories, exceptions, value_objects
from order_management import models as django_snapshots

class DjangoCustomerRepositoryImpl(repositories.CustomerAbstract):

    def get_customer_details(self, customer_id: str) -> value_objects.CustomerDetails:
        try:
            customer_details = django_snapshots.CustomerDetailsSnapshot.objects.get(
                customer_id=customer_id,
                is_active=True)
        except django_snapshots.CustomerDetailsSnapshot.DoesNotExist:
                raise exceptions.InvalidOrderOperation(f"Customer details for {customer_id} is not available.")

        return value_objects.CustomerDetails(
            first_name=customer_details.first_name,
            last_name=customer_details.last_name,
            email=customer_details.email
        )

    def get_shipping_address(self, customer_id: str) -> value_objects.Address:
        try:
            customer_address = django_snapshots.CustomerAddressSnapshot.objects.get(
                customer_id=customer_id,
                address_type="shipping",
                is_active=True)
        except django_snapshots.CustomerAddressSnapshot.DoesNotExist:
                raise exceptions.InvalidOrderOperation(f"Customer address for {customer_id} available.")

        return value_objects.Address(
            street=customer_address.street,
            city=customer_address.city,
            state=customer_address.state,
            postal=int(customer_address.postal_code),
            country=customer_address.country
        )

