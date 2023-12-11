from django.contrib import admin

from Hostel_app import models

# Register your models here.
admin.site.register(models.Student)
admin.site.register(models.Parent)
admin.site.register(models.Hostel)
admin.site.register(models.Fees)
