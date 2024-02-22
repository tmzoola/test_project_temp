from django.contrib import admin
from .models import Client,Employee,Product,Order
# Register your models here.

admin.site.register([Client,Employee,Product,Order])