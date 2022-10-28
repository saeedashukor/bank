from django.contrib import admin
from .models import AccountRecord, TransactionRecord

# Register your models here.
admin.site.register(AccountRecord)
admin.site.register(TransactionRecord)
