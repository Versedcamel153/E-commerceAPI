from django.contrib import admin
from .models import Developer, DeveloperAPIKey

# Register your models here.
admin.site.register(Developer)
admin.site.register(DeveloperAPIKey)
