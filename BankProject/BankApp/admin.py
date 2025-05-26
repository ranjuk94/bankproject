from django.contrib import admin
from .models import CustomUser, Customer

admin.site.register(CustomUser)


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'account_number', 'balance', 'dob', 'phone', 'aadhar_number', 'profile_image')
    search_fields = ('name', 'email', 'account_number')
    readonly_fields = ('profile_image',)
    list_filter = ('balance', 'dob', 'phone')
    fieldsets = (
        (None, {
            'fields': ('name', 'email', 'account_number', 'balance', 'dob', 'age', 'pan_number', 'address', 'phone',
                       'aadhar_number', 'profile_image')
        }),
    )
# Register the Customer model with the custom admin configuration
admin.site.register(Customer, CustomerAdmin)

from django.contrib import admin
from .models import Transaction

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('customer', 'branch', 'bank', 'ifsc', 'amount', 'balance', 'date', 'time')
    search_fields = ('customer__name', 'branch', 'bank', 'ifsc')
    list_filter = ('date', 'branch', 'bank')