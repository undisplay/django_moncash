from django.shortcuts import redirect

from django.http import Http404

from .utils import verify_payment
from .models import Transaction

def complete_transaction(request):

    transaction:Transaction = verify_payment(request).transaction

    if transaction:
        transaction.status = Transaction.Status.COMPLETE
        transaction.save()

        return redirect(transaction.return_url)
    else:
        return Http404()