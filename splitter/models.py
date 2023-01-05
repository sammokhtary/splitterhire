# ran command: python manage.py ogrinspect ukborders/data/GBR_adm2.shp UKBorder --srid=4326 --mapping --multi
# This is an auto-generated Django model module created by ogrinspect.

from django.contrib.gis.db import models
from django.core.validators import MinLengthValidator, EmailValidator, MinValueValidator, MaxValueValidator
from django.conf import settings


class ServiceArea(models.Model):
    country = models.CharField(max_length=75)
    area_name = models.CharField(max_length=75)
    area_geom = models.MultiPolygonField(srid=4326)

    # Reference many-many through table to keep track of companies in this ServiceArea
    companies = models.ManyToManyField('Company', through='ServicedArea')

# LayerMapping dictionary for ServiceArea model
servicearea_mapping = {
    'country': 'NAME_1',
    'area_name': 'NAME_2',
    'area_geom': 'MULTIPOLYGON',
}


class Company(models.Model) :
    name = models.TextField(
        validators=[MinLengthValidator(3, "Comment must be greater than 3 characters")]
    )

    # Reference many-many through table to keep track of areas this company services
    service_areas = models.ManyToManyField('ServiceArea', through='ServicedArea')


    #If user deletes their account we don't want company listing to be lost, so use SET_NULL
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)

    contact_phone = models.TextField(
        validators=[MinLengthValidator(11, "Phone number must have at least 11 digits")]
    )
    contact_email = models.TextField(
        validators=[EmailValidator()]
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        verbose_name_plural = 'companies'

    # Shows up in the admin list
    def __str__(self):
        if len(self.name) < 15 : return self.name
        return self.name[:11] + ' ...'

# The through table for many-many relationship between Company and ServiceArea
# Use SET.NULL because we don't want deleting companies or service areas to affect our company or area listings.
class ServicedArea(models.Model) :

    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    service_area = models.ForeignKey(ServiceArea, on_delete=models.CASCADE)


class Make(models.Model) :
    name = models.TextField(
        validators=[MinLengthValidator(3, "Comment must be greater than 3 characters")]
    )

    # Shows up in the admin list
    def __str__(self):
        if len(self.name) < 15 : return self.name
        return self.name[:11] + ' ...'


class VehicleModel(models.Model) :
    name = models.TextField(
        validators=[MinLengthValidator(3, "Comment must be greater than 3 characters")]
    )

    #use SET_NULL because makes will be deleted by admins not users, so we want to avoid accidentally deleting models due to admin error
    make = models.ForeignKey(Make, on_delete=models.SET_NULL, null=True)

    # Shows up in the admin list
    def __str__(self):
        if len(self.name) < 15 : return self.name
        return self.name[:11] + ' ...'


class Splitter(models.Model) :

    #Reference the Company table, if company is deleted the listing is deleted
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    #Reference the Model table - use SET_NULL because models will be deleted by admins
    #not users, so we want to avoid accidentally deleting listings due to admin error
    vehicle_model = models.ForeignKey(VehicleModel, on_delete=models.SET_NULL, null=True)

    seats = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
        )

    fee = models.DecimalField(max_digits=7, decimal_places=2, null=True)

    comments = models.TextField(blank=True)

    trailer = models.BooleanField(default=False)

    selfhire = models.BooleanField(default=False)

    tourmanager = models.BooleanField(default=False)

    sleeper = models.BooleanField(default=False)

    foh = models.BooleanField(default=False)

    lampy = models.BooleanField(default=False)

    tech = models.BooleanField(default=False)