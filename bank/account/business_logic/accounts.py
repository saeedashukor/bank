from ..models import AccountRecord, AuditRecord, TransactionRecord
import abc


class Account:

    def __init__(self, account_id):
        self.account_id = account_id
        self._balance = self.calc_balance()
        self.account_type = 'current'

    @property
    def balance(self):
        return self._balance

    @balance.setter
    def balance(self, new_balance):
        new_audit_record = AuditRecord.objects.create(old_balance=self.balance,
                                                      new_balance=new_balance)
        new_audit_record.save()
        self._balance = new_balance

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
        new_deposit_record = TransactionRecord.objects.create(transaction_type='DEPOSIT',
                                                              source=None,
                                                              target=account,
                                                              amount=amount)
        new_deposit_record.save()

    def withdraw(self, amount):
        self.balance -= amount
        account = AccountRecord.objects.get(pk=self.account_id)
        new_withdraw_record = TransactionRecord.objects.create(transaction_type='WITHDRAW',
                                                               source=account,
                                                               target=None,
                                                               amount=amount)
        new_withdraw_record.save()

    def transfer_in(self, amount, source_id):
        print(source_id)
        self.balance += amount

        # Update balance of source_id
        source_account = accounts[source_id]
        source_account.balance -= amount

        source_account = AccountRecord.objects.get(pk=source_id)
        target_account = AccountRecord.objects.get(
            pk=self.account_id)  # we are the target because money is being transferred in
        new_transfer_record = TransactionRecord.objects.create(transaction_type='TRANSFER',
                                                               source=source_account,
                                                               target=target_account,
                                                               amount=amount)
        new_transfer_record.save()


class InterestMixin(abc.ABC):
    def apply_monthly_interest(self, monthly_percentage):
        interest = self.balance * (float(monthly_percentage) / 100)
        self.balance += interest

        account = AccountRecord.objects.get(pk=self.account_id)
        new_transaction = TransactionRecord.objects.create(transaction_type='INTEREST',
                                                           source=None,
                                                           target=account,
                                                           amount=interest)
        new_transaction.save()


class SavingsAccount(Account, InterestMixin):
    def __init__(self, account_id):
        super().__init__(account_id)
        self.interest_rate = 0.5  # default interest rate for savings account
        self.account_type = 'savings'


class SuperSavingsAccount(Account, InterestMixin):
    def __init__(self, account_id):
        super().__init__(account_id)
        self.interest_rate = 0.7  # default interest rate for super_savings account
        self.account_type = 'super_savings'


class Accounts:

    def __init__(self):
        self.accounts_dict = {}

    def __getitem__(self, item):
        self.create_accounts()
        return self.accounts_dict[item]

    # Factory Method is a design pattern used to create concrete implementations of a common interface
    # It separates the process of creating an object from the code that depends on the interface of the project
    def account_factory(self, account):
        if account.account_type == 'CURRENT':
            return Account(account.id)
        elif account.account_type == 'SAVINGS':
            return SavingsAccount(account.id)
        else:
            return SuperSavingsAccount(account.id)

    def create_accounts(self):
        account_records = AccountRecord.objects.all()
        for account in account_records:
            self.accounts_dict[account.id] = self.account_factory(account)


accounts = Accounts()
