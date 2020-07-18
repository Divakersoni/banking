from django.contrib import admin
from customer.models import AccountTransaction, AccountDetails
# Register your models here.
admin.site.register(AccountTransaction)
admin.site.register(AccountDetails)