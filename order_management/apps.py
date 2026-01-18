from django.apps import AppConfig


class OrderManagementConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'order_management'

    def ready(self):
        #load bootstrap is good enough

        #from ddd.order_management.infrastructure.bootstrap import bootstrap_aws

        from ddd.order_management.infrastructure.bootstrap import bootstrap_onprem

        print("Order Management initialization complete. To enable on-premise infrastructure, ensure you invoke the bootstrap handler: \n" \
        "from ddd.order_management.infrastructure.bootstrap import bootstrap_onprem")



