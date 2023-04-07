[![moncash](https://sandbox.moncashbutton.digicelgroup.com/Moncash-middleware/resources/assets/images/MC_button.png)](https://sandbox.moncashbutton.digicelgroup.com/)

# Digicel Moncash API SDK for DJANGO


Digicel MonCash - MonCash is a mobile wallet that facilitates reliable, safe and convenient financial transactions to reduce the distance between people regardless of their location in Haiti. While providing its services to its customer base of over 1.5 million people, MonCash maintains its goal of expanding its range of available services.

## Define: SDK
> SDK stands for “Software Development Kit”, which is a great way to think about it — a kit.
> Think about putting together a model car or plane. When constructing this  model, a whole kit of items is needed, including the kit pieces themselves, the tools needed to put them together, assembly instructions, and so forth.

## Features
- Create payment
- Consume payment
- Verify payment

## Installation
Moncash requires [DJANGO](https://www.djangoproject.com) v2.2+ to run.
_Install the the SDK and start using it._

Install using pip with:

```sh
    pip install  django_moncash
```
Add django_moncash app to INSTALLED_APPS in your django settings.py:

```python
    INSTALLED_APPS = (
        ...,
        'django_moncash',
    )
```

## Configuring the client
Digicel Moncash API [Dashboard](https://sandbox.moncashbutton.digicelgroup.com/Moncash-business/Login).
_Each business has it's own `clientId` `clientSecret` pairs._

Add credentials in your django settings.py:
```python

    MONCASH = {
        'CLIENT_ID':'YOUR_CLIENT_ID',
        'SECRET_KEY':'YOUR_SECRET_KEY',
        'ENVIRONMENT':'sandbox or production'
    }

```

Include django_moncash.urls in your django project urls.py:

```python

    from django.contrib import admin
    from django.urls import path,include

    urlpatterns = [
        path('admin/', admin.site.urls),
        path('payment/',include('django_moncash.urls')),

        path('',include('test_app.urls'))
    ]

```

On the Digicel Moncash API [Dashboard](https://sandbox.moncashbutton.digicelgroup.com/Moncash-business/Login) 
setup the business return url to be "https://yoursite.com/payment/moncash"

Note that "payment" is the base route you chose when your urls.py (path('payment/',include('django_moncash.urls')))

## Create Payment
The only supported currency is 'HTG'.
_With the configue above._
```python

    from django.shortcuts import redirect

    from django_moncash.utils import init_payment

    #views
    def buy(request):

        """ 
        params:

            request,                  # django views request
            amount: float,            # amount to pay
            return_url: str = None,   # custom return_url, default to current view
            order_id: str = None,     # unique order_id, default uuidV4
            meta_data: dict = None    # meta_data associated to the request
        """
        payment = init_payment(request,50)
        

        print(payment)

        return redirect(payment['payment_url'])

    """ output:
        {
            "payment_url":https://'<sandbox|"">'.moncashbutton.digicelgroup.com/Moncash-middleware/Payment/Redirect?token='<token>',
            "transaction":Transaction<object>
        }
    """
```

## Verify Payment
Two way to do so.
_By moncash_transaction_id or request if on the "return_url" view._
```python
    from django.http import HttpResponse

    from django_moncash.utils import verify_payment

    #views
    def verify(request):
    
        """ 
        params:

            request,                             # django views request
            moncash_transaction_id: str = None   # custom moncash_transaction_id, default to "request.GET.get("transactionId",None)"
        """

        payment = verify_payment(request)

        print(payment)

        return HttpResponse("payment succeed.")

    """ output:
        {
            "transaction": Transaction<object>,
            "transactionId":"XXXXXXXXXX"
        }
    """

```

## Consume Payment
Two way to do so.
_By moncash_transaction_id or request if on the "return_url" view._
```python
    from django.http import HttpResponse

    from django_moncash.utils import consume_payment

    #views
    def consume(request):
    
        """ 
        params:

            request,                             # django views request
            moncash_transaction_id: str = None   # custom moncash_transaction_id, default to "request.GET.get("transactionId",None)"
        """

        result = consume_payment(request)

        print(result)

        if result["success"]:

            return HttpResponse("payment successfuly consume.")
        
        return HttpResponse("payment failed to be consumed.")

    """ output:
        # if already consume
        {
            "success":False,
            "error":"USED",
            "payment":{
                "transaction": Transaction<object>,
                "transactionId":"XXXXXXXXXX"
            }
        }

        # if not found
        {
            "success":False,
            "error":"NOT_FOUND"
        }

        # if consume successfuly
        {
            "success":True,
            "payment":{
                "transaction": Transaction<object>,
                "transactionId":"XXXXXXXXXX"
            }
        }
    """

```

The difference between verify_payment and consume is that verify_payment didn't change the status of the transaction
```python

    #Possible transaction status

    from django_moncash.models import Transaction

    Transaction.Status.PENDING      # before payment
    Transaction.Status.COMPLETE     # after payment
    Transaction.Status.CONSUME      # after consume

```


## Error handling
List of errors in moncash.exceptions
```python
    from moncash.exceptions import  NotFoundError

    from django.db import IntegrityError 

    from django_moncash.models import Transaction
```
# List of errors 
From moncash
- AuthenticationError
- AuthorizationError
- GatewayTimeoutError
- ConnectionError
- InvalidResponseError
- ConnectTimeoutError
- ReadTimeoutError
- TimeoutError
- NotFoundError
- RequestTimeoutError
- ServerError
- ServiceUnavailableError
- TooManyRequestsError
- UnexpectedError
- UpgradeRequiredError

From django
- IntegrityError 
- Transaction.DoesNotExist

## Current Transaction model

```python

    class Transaction(models.Model):

        class Status(models.TextChoices):
            PENDING = 'PENDING', _("Pending")
            COMPLETE = 'COMPLETE', _("Complete")
            CONSUME = 'CONSUME', _("Consume")


        user = models.ForeignKey(
            User,
            on_delete=models.SET_NULL,
            null=True,
            blank=True
        )

        order_id = models.CharField(_("Order id"), max_length=50,default=uuid.uuid4,unique=True, editable=False)
        amount   = models.DecimalField(_("Amount"), max_digits=11, decimal_places=2,blank=False,null=False)
        status = models.CharField(_('Status'),max_length=25,choices=Status.choices,default=Status.PENDING,blank=False)

        return_url = models.TextField(_("Return URL"),blank=False,null=False)

        meta_data = models.JSONField(_("Meta data"),null=True,blank=True)
        
        created_at = models.DateTimeField(auto_now_add=True)
        updated_at = models.DateTimeField(auto_now=True)
```

## Development
Run all tests.
```sh
    python load_tests.py
```

## Donate to support us

Scan and donate using the Moncash App

![Moncash_QR](https://i.ibb.co/mDmPCHj/qr.jpg)  

Or send to 
(+509) 48-02-0151

## License
[GNU GENERAL PUBLIC LICENSE](https://www.gnu.org/licenses/gpl-3.0.txt)
_Version 3, 29 June 2007_

## Useful links
- [Pypi package link](https://pypi.org/project/django-moncash/)
- [Digicel Moncash API Dashboard](https://sandbox.moncashbutton.digicelgroup.com)
- [RestAPI_MonCash_doc.pdf](https://sandbox.moncashbutton.digicelgroup.com/Moncash-business/resources/doc/RestAPI_MonCash_doc.pdf)
- [Low level SDK for python](https://github.com/dokla/moncash_python)
