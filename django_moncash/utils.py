from django.conf import settings 


from .models import Transaction


import moncash

from moncash.exceptions import  NotFoundError

environment = moncash.environment.Sandbox

if str.lower(settings.MONCASH['ENVIRONMENT']) == 'production':
    environment = moncash.environment.Production

gateway = moncash.Moncash(
    client_id=settings.MONCASH['CLIENT_ID'],
    client_secret=settings.MONCASH['SECRET_KEY'],
    environment= environment
)

def init_payment(request,amount: float,return_url: str = None,order_id: str=None,meta_data: dict=None):

    amount = float(amount)

    if not return_url:
        return_url = request.get_full_path()

    if order_id:
        transaction = Transaction.objects.create(user=request.user,amount=amount,return_url=return_url,meta_data=meta_data,order_id=order_id)
    else:
        transaction = Transaction.objects.create(user=request.user,amount=amount,return_url=return_url,meta_data=meta_data)

    payment_url = gateway.payment.create(amount=transaction.amount, reference=str(transaction.order_id))

    return {
        "payment_url":payment_url,
        "transaction":transaction
    }


def verify_payment(request,moncash_transaction_id: str=None):

    if not moncash_transaction_id:
        moncash_transaction_id = request.GET.get("transactionId",None)

    transaction = {}

    try:
        transaction = gateway.payment.get_by_id(transactionId=moncash_transaction_id)
    except NotFoundError:
        transaction["reference"] = None


    try:
        transaction = Transaction.objects.get(order_id=transaction["reference"])
    except Transaction.DoesNotExist:
        transaction = None

    return {
        "transaction": transaction,
        "transactionId":moncash_transaction_id
    }


def consume_payment(request,moncash_transaction_id: str=None):

    payment = None

    if moncash_transaction_id:
        payment = verify_payment(moncash_transaction_id=moncash_transaction_id)
    else:
        payment = verify_payment(request)

    if payment['transaction']:

        if payment['transaction'].status == Transaction.Status.CONSUME:
            return {
                "success":False,
                "error":"USED",
                "payment":payment
            }
        
        payment['transaction'].status = Transaction.Status.CONSUME
        payment['transaction'].save()

        return {
            "success":True,
            "payment":payment
        }
            
      
    return {
        "success":False,
        "error":"NOT_FOUND"
    }