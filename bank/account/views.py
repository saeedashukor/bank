from django.shortcuts import render
from .models import AccountRecord, AuditRecord, TransactionRecord
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
