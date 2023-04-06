
from django.urls import path

from .views import *

urlpatterns = [
    path('moncash/',complete_transaction, name='django_moncash_return_url'),
]
