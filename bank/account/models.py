from django.db import models


class AccountRecord(models.Model):
    class AccountChoices(models.TextChoices):
        savings = ('SAVINGS', 'savings')
        super_savings = ('SUPER_SAVINGS', 'super_savings')
        current = ('CURRENT', 'current')

    name = models.CharField(max_length=100)
    account_type = models.CharField(max_length=32, choices=AccountChoices.choices, default=AccountChoices.current)

    def __str__(self):
        return f' {self.name}, {self.account_type}'


class TransactionRecord(models.Model):
    class TransactionChoices(models.TextChoices):
        deposit = ('DEPOSIT', 'deposit')
        withdraw = ('WITHDRAW', 'withdraw')
        transfer = ('TRANSFER', 'transfer')
        interest = ('INTEREST', 'interest')

    transaction_type = models.CharField(max_length=32, choices=TransactionChoices.choices)
    source = models.ForeignKey(AccountRecord, related_name='source', on_delete=models.CASCADE, null=True, blank=True)
    target = models.ForeignKey(AccountRecord, related_name='target', on_delete=models.CASCADE, null=True, blank=True)
    amount = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f' {self.transaction_type} : {self.source}, {self.target}, {self.amount}, {self.created}'


class AuditRecord(models.Model):
    account_record = models.ForeignKey(AccountRecord, on_delete=models.CASCADE, null=True, blank=True)
    old_balance = models.IntegerField()
    new_balance = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f' {self.account_record} : {self.old_balance} (old), {self.new_balance} (new), {self.created}'


