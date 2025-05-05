from django.apps import AppConfig
class YourAppConfig(AppConfig):
    name = 'products'

    def ready(self):
        import products.signals
