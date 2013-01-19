from django.contrib import admin
from account.models import RetailerAccount, UserAccount, Employee


class RetailerAccountAdmin(admin.ModelAdmin):
    model = RetailerAccount

admin.site.register(RetailerAccount, RetailerAccountAdmin)

class UserAccountAdmin(admin.ModelAdmin):
    model = UserAccount

class EmployeeAdmin(admin.ModelAdmin):
    model = Employee

admin.site.register(Employee, EmployeeAdmin)

admin.site.register(UserAccount, UserAccountAdmin)
