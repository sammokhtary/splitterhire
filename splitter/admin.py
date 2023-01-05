from django.contrib.gis import admin
from .models import ServiceArea, Company, Make, VehicleModel, Splitter, ServicedArea

@admin.register(ServiceArea)
class ServiceAreaAdmin(admin.OSMGeoAdmin):
    list_display = ("country", "area_name")

admin.site.register(Company)
admin.site.register(ServicedArea)
admin.site.register(Make)
admin.site.register(VehicleModel)
admin.site.register(Splitter)