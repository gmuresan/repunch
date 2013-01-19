from django.contrib import admin
from retailer.forms import NewRetailerForm
from retailer.models import Retailer
    

class RetailerAdmin(admin.ModelAdmin):
    model = Retailer
    inlines = []
    form = NewRetailerForm

admin.site.register(Retailer, RetailerAdmin)
