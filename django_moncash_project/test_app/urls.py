
from django.urls import path

from .views import *

urlpatterns = [
    path('',index,name='test_app_home'),
    path('buy/<int:id>/',buy,name='test_app_buy')
]
