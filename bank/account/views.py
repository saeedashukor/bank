from django.shortcuts import render
from django.db.models import Q
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
    account_id = [account.id for account in AccountRecord.objects.filter(
        Q(account_type='SAVINGS') | Q(account_type='SUPER_SAVINGS'))]
    balances = {}
    for id_ in account_id:
        name = AccountRecord.objects.get(pk=id_).name
        account_type = AccountRecord.objects.get(pk=id_).account_type
        balance = accounts[id_].balance
        balances[id_] = {'name': name,
                         'type': account_type,
                         'balance': balance}
    context = {'acc_balances': balances}

    if request.method == 'POST':
        interest = request.POST['interest']
        for i in range(len(account_id)):
            # If interest rate not specified, use default interest rate based on account_type
            if not interest or interest == 0.0:
                default_interest = accounts[account_id[i]].interest_rate
                accounts[account_id[i]].apply_monthly_interest(default_interest)
            else:
                accounts[account_id[i]].apply_monthly_interest(float(interest))

    return render(request, 'account/monthly_interest.html', context)
