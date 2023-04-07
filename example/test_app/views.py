from django.shortcuts import render,redirect

from django_moncash.utils import init_payment,verify_payment,consume_payment

def index(request):
    return render(request,"test_app/index.html")

def buy(request,id):
    if consume_payment(request)['success']:
        return render(request,"test_app/index.html",{"payed":True})
    else:
        return redirect(init_payment(request,50)['payment_url'])