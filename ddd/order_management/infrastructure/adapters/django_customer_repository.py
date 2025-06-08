from ddd.order_management.domain import repositories, exceptions
from order_management import models as django_snapshots

class DjangoCustomerRepositoryImpl(repositories.CustomerAbstract):

    def get_customer_details(self, customer_id: str):
        customer_details = django_snapshots.CustomerDetailsSnapshot.objects.filter(
            customer_id=customer_id, 
            addresses__address_type="shipping", 
            addresses__is_default=True
        ).values(
            'user__first_name', 
            'user__last_name', 
            'user__email', 
            'addresses__street', 
            'addresses__city', 
            'addresses__state', 
            'addresses__postal_code', 
            'addresses__country'
        ).first()

        if not customer_details: 
            raise exceptions.InvalidOrderOperation("Customer record not available.")

        return {
            'first_name': customer_details.get('user__first_name'),
            'last_name': customer_details.get('user__last_name'),
            'email': customer_details.get('user__email'),
            'street': customer_details.get('addresses__street'),
            'city': customer_details.get('addresses__city'),
            'state': customer_details.get('addresses__state'),
            'postal_code': customer_details.get('addresses__postal_code'),
            'country': customer_details.get('addresses__country')
        }
