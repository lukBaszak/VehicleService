from django.contrib import admin

# Register your models here.
from Service.models import Vehicle, VehicleType, PropertyVehicle, ServiceTransaction, ServiceFinancialTransaction, \
    Service, ServiceItem



class ServiceFinancialTransactionAdmin(admin.ModelAdmin):
    readonly_fields = ['gross_price']


class ServiceItemInline(admin.StackedInline):
    model = ServiceItem
    extra = 0


class ServiceTransactionAdmin(admin.ModelAdmin):
    readonly_fields = ["transaction_number"]
    inlines = [ServiceItemInline]

admin.site.register(Vehicle)
admin.site.register(VehicleType)
admin.site.register(PropertyVehicle)
admin.site.register(ServiceTransaction,ServiceTransactionAdmin)
admin.site.register(ServiceFinancialTransaction, ServiceFinancialTransactionAdmin)
admin.site.register(Service)
admin.site.register(ServiceItem)