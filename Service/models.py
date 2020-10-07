from datetime import datetime

from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


# Create your models here.
from django.utils import timezone


class VehicleType(models.Model):

    name = models.CharField(max_length=40, null=False, blank=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Typ pojazdu'
        verbose_name_plural = 'Typy pojazdów'




class Vehicle(models.Model):

    vehicle_type = models.ForeignKey(to=VehicleType, on_delete=models.PROTECT, verbose_name="Typ pojazdu")
    manufacturer = models.CharField(max_length=30, null=True, blank=True, verbose_name='Producent')
    model = models.CharField(max_length=50, null=False, blank=True, default='-', verbose_name="Model pojazdu")

    def __str__(self):
        return f"[{self.vehicle_type.name.upper()}] {self.model}"

    class Meta:
        verbose_name = 'Pojazd'
        verbose_name_plural = 'Pojazdy'


class PropertyVehicle(models.Model):

    vehicle = models.ForeignKey(to=Vehicle, on_delete=models.PROTECT, verbose_name='Model pojazdu')
    serial_number = models.CharField(max_length=50, null=True, blank=True, verbose_name='Numer seryjny')
    user = models.ForeignKey(to=User, on_delete=models.PROTECT, verbose_name='Właściciel')
    vehicle_mileage = models.IntegerField(null=True, blank=True, verbose_name="Przebieg")

    def __str__(self):
        return f"{self.user.email} - {self.vehicle.model}"

    class Meta:
        verbose_name = 'Pojazd użytkownika'
        verbose_name_plural = 'Pojazdy użytkownika'


class ServiceTransaction(models.Model):

    reception_type = [
        ("PERSONAL_PICKUP", "Personal Pickup"),
        ("COURIER", "Courier")
    ]

    client = models.ForeignKey(to=User, on_delete=models.PROTECT, verbose_name="Klient")
    transaction_number = models.CharField(max_length=50, null=False, blank=True, unique=True)
    way_of_reception = models.CharField(max_length=40, choices=reception_type, null=False, blank=True, default="PERSONAL_PICKUP", verbose_name="Sposób odbioru")
    generation_date = models.DateTimeField(editable=True, auto_now_add=True, verbose_name='Utworzony')
    service_description = models.TextField(max_length=300, null=True, blank=True)

    def __str__(self):
        return f"{self.client.email} - {self.transaction_number}"

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None, *args, **kwargs):
        try:
            latest_id = ServiceTransaction.objects.latest('id').id

        except ServiceTransaction.DoesNotExist:
            latest_id = 0000

        self.transaction_number = f"RMA/{latest_id+1}/{datetime.today().year}"
        super(ServiceTransaction, self).save(*args, **kwargs)
    class Meta:
        verbose_name = "Usługa naprawy"
        verbose_name_plural = "Usługi naprawy"


def gross_price(tax_rate):
    return lambda net_price: net_price + net_price*(tax_rate/100)

class ServiceFinancialTransaction(models.Model):

    service_transaction = models.ForeignKey(ServiceTransaction, on_delete=models.PROTECT)
    warranty_repairment = models.BooleanField(default=False, verbose_name="Naprawa gwarancyjna")
    net_price = models.DecimalField(decimal_places=2, max_digits=6, default=0)
    gross_price = models.DecimalField(decimal_places=2, max_digits=6, default=0)
    tax_rate = models.DecimalField(default=23, decimal_places=1, max_digits=3, validators=[MaxValueValidator(limit_value=100), MinValueValidator(limit_value=0)], verbose_name="Vat [%]")

    class Meta:
        verbose_name = "Transakcja finansowa"
        verbose_name_plural = "Transakcje finansowe"

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.recalculate_price()

        super(ServiceFinancialTransaction, self).save()

    def recalculate_price(self):
        self.gross_price = gross_price(self.tax_rate)(self.net_price)



fs = FileSystemStorage(location='/media/services_photos')

class Service(models.Model):

    title = models.CharField(max_length=60, null=False, blank=False)
    net_price = models.DecimalField(max_digits=6, decimal_places=2)
    description = models.TextField()
    image = models.ImageField(upload_to='services_photos/')

    def __str__(self):
        return self.title

class ServiceItem(models.Model):

    service_transaction = models.ForeignKey(ServiceTransaction, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.PROTECT)
    quantity = models.PositiveSmallIntegerField(default=1)



