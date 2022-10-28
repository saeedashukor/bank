from ..models import AccountRecord, TransactionRecord

'''
    transaction_choices = [
        (1, 'deposit'),
        (2, 'withdrawal'),
        (3, 'transfer')
    ]
'''


class Account:

    def __init__(self, account_id):
        self.account_id = account_id
        self.balance = self.calc_balance()

    def calc_balance(self):
        # Add target deduct source
        target_records = sum(
            [transaction.amount for transaction in TransactionRecord.objects.filter(target=self.account_id)])
        source_records = sum(
            [transaction.amount for transaction in TransactionRecord.objects.filter(source=self.account_id)])
        return target_records - source_records

    def deposit(self, amount):
        self.balance += amount
        account = AccountRecord.objects.get(pk=self.account_id)
        new_deposit_record = TransactionRecord.objects.create(transaction_type=1,
                                                              source=None,
                                                              target=account,
                                                              amount=amount)
        new_deposit_record.save()

    def withdraw(self, amount):
        self.balance -= amount
        account = AccountRecord.objects.get(pk=self.account_id)
        new_withdraw_record = TransactionRecord.objects.create(transaction_type=2,
                                                               source=account,
                                                               target=None,
                                                               amount=amount)
        new_withdraw_record.save()

    def transfer_in(self, amount, source_id):
        self.balance += amount

        # Update balance of source_id
        source_account = accounts[source_id]
        source_account.balance -= amount

        source_account = AccountRecord.objects.get(pk=source_id)
        target_account = AccountRecord.objects.get(
            pk=self.account_id)  # we are the target because money is being transferred in
        new_transfer_record = TransactionRecord.objects.create(transaction_type=3,
                                                               source=source_account,
                                                               target=target_account,
                                                               amount=amount)
        new_transfer_record.save()


class Accounts:

    def __init__(self):
        self.accounts_dict = {}
        self.create_accounts()

    def __getitem__(self, item):
        return self.accounts[item]

    def create_accounts(self):
        account_records = AccountRecord.objects.all()
        for account in account_records:
            self.accounts_dict[account.id] = Account(account.id)


accounts = Accounts()
