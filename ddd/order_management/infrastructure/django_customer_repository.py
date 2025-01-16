from ddd.order_management.domain import repositories, exceptions
from customer_management import models as django_customer_models

class DjangoCustomerRepository(repositories.CustomerRepository):

    def get_customer_details(self, customer_id: str):
        customer_details = django_customer_models.Customer.objects.filter(
                                        customer_id=customer_id, 
                                        addresses__address_type="shipping", 
                                        addresses__is_default=True).values(
                                                'user__first_name', 
                                                'user__last_name', 
                                                'user__email', 
                                                'addresses__street', 
                                                'addresses__city', 
                                                'addresses__state', 
                                                'addresses__postal_code', 
                                                'addresses__country'
                                            )
        if customer_details.exists():
            return {
                'first_name': customer_details[0].get('user__first_name'),
                'last_name': customer_details[0].get('user__last_name'),
                'first_name': customer_details[0].get('user__email'),
                'street': customer_details[0].get('addresses__street'),
                'city': customer_details[0].get('addresses__city'),
                'state': customer_details[0].get('addresses__state'),
                'postal_code': customer_details[0].get('addresses__postal_code'),
                'country': customer_details[0].get('addresses__country'),
            }
        else:
            raise exceptions.InvalidOrderOperation("Customer record not available.")
