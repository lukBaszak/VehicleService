from django.apps import AppConfig
# from django.db.models.signals import post_save
#
# from Service.models import ServiceTransaction
# from Service.signals import create_service_transaction
#

class ServiceConfig(AppConfig):
    name = 'Service'

    def ready(self):
        import Service.signals
    #     post_save.connect(create_service_transaction, sender=ServiceTransaction)
