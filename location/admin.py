from django.contrib import admin
from location.models import Zip

class ZipAdmin(admin.ModelAdmin):
    model = Zip

admin.site.register(Zip, ZipAdmin)

