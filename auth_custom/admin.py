from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin
from auth_custom import models




additional_fields = ('full_name', 'phone', 'role')

UserAdmin.list_display += additional_fields
UserAdmin.list_filter += additional_fields
UserAdmin.fieldsets += (('Extra Fields', {'fields': additional_fields}),)
admin.site.register(models.User, UserAdmin)
