from django.apps import AppConfig


class OrderManagementConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'order_management'

    def ready(self):
        from ddd.order_management.infrastructure import bootstrap
        bootstrap.register()

