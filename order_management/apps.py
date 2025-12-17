from django.apps import AppConfig


class OrderManagementConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'order_management'

    def ready(self):
        #load bootstrap is good enough

        #from ddd.order_management.infrastructure.bootstrap import bootstrap_aws

        from ddd.order_management.infrastructure.bootstrap import bootstrap_onprem



