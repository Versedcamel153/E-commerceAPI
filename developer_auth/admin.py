from django.contrib import admin
from .models import Developer, DeveloperAPIKey, APIKey

# Register your models here.
admin.site.register(Developer)
admin.site.register(DeveloperAPIKey)
admin.site.register(APIKey)