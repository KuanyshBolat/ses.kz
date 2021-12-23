from django.contrib import admin
from business import models


@admin.register(models.Company)
class CompanyAdmin(admin.ModelAdmin):
    pass


@admin.register(models.BusinessCenter)
class BusinessCenterAdmin(admin.ModelAdmin):
    pass


@admin.register(models.BusinessCenterOffice)
class BusinessCenterOfficeAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Things)
class ThingsAdmin(admin.ModelAdmin):
    pass
