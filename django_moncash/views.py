from django.shortcuts import redirect,resolve_url

from django.http import Http404

from .utils import verify_payment
from .models import Transaction

from ._utils import add_params

def complete_transaction(request):

    payment = verify_payment(request)

    transaction:Transaction = payment['transaction']

    if transaction:
        transaction.status = Transaction.Status.COMPLETE
        transaction.transaction_id = payment['transactionId']
        transaction.save()

        return redirect(add_params(resolve_url(transaction.return_url),{"transactionId":payment['transactionId']}))
    else:
        raise Http404