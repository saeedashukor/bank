from django.contrib import admin
from .models import AccountRecord, AuditRecord, TransactionRecord

# Register your models here.
admin.site.register(AccountRecord)
admin.site.register(TransactionRecord)
admin.site.register(AuditRecord)

