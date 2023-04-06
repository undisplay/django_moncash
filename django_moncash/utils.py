from django.urls import resolve
from django.conf import settings 


from .models import Transaction


import moncash

environment = moncash.environment.Sandbox

if str.lower(settings.MONCASH['ENVIRONMENT']) is 'production':
    environment = moncash.environment.Production

gateway = moncash.Moncash(
    client_id=settings.MONCASH['CLIENT_ID'],
    client_secret=settings.MONCASH['SECRET_KEY'],
    environment= environment
)


def init_payment(request,amonut: float,return_url: str,cancel_url: str,order_id: str,meta_data: dict):

    if not return_url:
        return_url = resolve(request.path_info).url_name

    if not cancel_url:
        cancel_url = resolve(request.path_info).url_name

    if order_id:
        transaction = Transaction.objects.create(amonut=amonut,return_url=return_url,cancel_url=cancel_url,meta_data=meta_data,order_id=order_id)
    else:
        transaction = Transaction.objects.create(amonut=amonut,return_url=return_url,cancel_url=cancel_url,meta_data=meta_data)

    payment_url = gateway.payment.create(amount=transaction.amount, reference=str(transaction.order_id))

    return {
        "payment_url":payment_url,
        "transaction":transaction
    }


def verify_payment(request,moncash_transaction_id: str):

    if not moncash_transaction_id:
        moncash_transaction_id = request.GET.get("transactionId",None)

        try:
            gateway.payment.get_by_id(transactionId=moncash_transaction_id)

            transaction = Transaction.objects.get(order_id=transaction["reference"])
        except:
            transaction = None

    return {
        "transaction": transaction
    }


def consume_payment(request,order_id: str):
    if order_id:
        payment = verify_payment(moncash_transaction_id=order_id)
    else:
        payment = verify_payment(request)

    if payment.transaction:
        payment.transaction.status = Transaction.Status.CONSUME
        payment.transaction.save()
      
    return payment