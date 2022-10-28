from django.db import models
from django.utils import timezone


# Create your models here.
class AccountRecord(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class TransactionRecord(models.Model):
    transaction_choices = [
        (1, 'deposit'),
        (2, 'withdrawal'),
        (3, 'transfer')
    ]
    transaction_type = models.CharField(max_length=32, choices=transaction_choices)
    source = models.ForeignKey(AccountRecord, related_name='source', on_delete=models.CASCADE, null=True, blank=True)
    target = models.ForeignKey(AccountRecord, related_name='target', on_delete=models.CASCADE, null=True, blank=True)
    amount = models.IntegerField()
    created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f' {self.transaction_type} : {self.transaction_choices[int(self.transaction_type)-1]}, {self.source}, {self.target}, {str(self.amount)}, {str(self.created)}'


