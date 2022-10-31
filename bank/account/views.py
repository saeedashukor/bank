from django.shortcuts import render
from .models import AccountRecord
from django.views import generic
from .business_logic.accounts import accounts


class IndexView(generic.ListView):
    template_name = 'account/index.html'
    context_object_name = 'account_records'

    def get_queryset(self):
        return AccountRecord.objects.all()


def withdraw(request):
    account_record = AccountRecord.objects.all()
    context = {'account_record': account_record}

    if request.method == 'POST':
        account_id = int(request.POST['account'].split(',')[0])
        amount = int(request.POST['amount'])
        accounts[account_id].withdraw(amount)

    return render(request, 'account/withdraw.html', context)


def deposit(request):
    account_record = AccountRecord.objects.all()
    context = {'account_record': account_record}

    if request.method == 'POST':
        account_id = int(request.POST['account'].split(',')[0])
        amount = int(request.POST['amount'])
        accounts[account_id].deposit(amount)

    return render(request, 'account/deposit.html', context)


def transfer(request):
    account_record = AccountRecord.objects.all()
    context = {'account_record': account_record}

    if request.method == 'POST':
        source_id = int(request.POST['source_account'].split(',')[0])
        target_id = int(request.POST['target_account'].split(',')[0])
        amount = int(request.POST['amount'])
        accounts[target_id].transfer_in(amount, source_id)

    return render(request, 'account/transfer.html', context)


def monthly_interest(request):
    account_id = [account.id for account in AccountRecord.objects.filter(account_type='SAVINGS')]
    balances = {}
    for id_ in account_id:
        name = AccountRecord.objects.get(pk=id_).name
        balance = accounts[id_].balance
        balances[id_] = {'name': name,
                         'balance': balance}
    context = {'acc_balances': balances}

    if request.method == 'POST':
        interest = float(request.POST['interest'])
        for i in range(len(account_id)):
            accounts[account_id[i]].apply_monthly_interest(interest)

    return render(request, 'account/monthly_interest.html', context)
