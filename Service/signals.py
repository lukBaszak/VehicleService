from django.db.models.signals import post_save
from django.dispatch import receiver

import RepairService
from Service.models import ServiceFinancialTransaction, ServiceTransaction, ServiceItem, Service


@receiver(signal=post_save, sender=ServiceTransaction)
def create_service_transaction(sender, instance, created, **kwargs):
    if created:
        ServiceFinancialTransaction.objects.create(service_transaction=instance)


@receiver(signal=post_save, sender=ServiceItem)
def calculus_price_handler(sender, instance, created, **kwargs):

    financial_transaction = ServiceFinancialTransaction.objects.get(service_transaction__serviceitem=instance)
    price_handler = calculate_price(instance.quantity)
    financial_transaction.net_price += price_handler(Service.objects.get(serviceitem=instance).net_price)
    financial_transaction.save()

def calculate_price(quantity):
    return lambda net_price: net_price * quantity


