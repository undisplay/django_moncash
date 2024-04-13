from django.contrib import admin

# Register your models here.
# vim: set fileencoding=utf-8 :
from django.contrib import admin

import django_moncash.models as models


class TransactionAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'user',
        'order_id',
        'transaction_id',
        'amount',
        'status',
        'return_url',
        'meta_data',
        'created_at',
        'updated_at',
    )
    list_filter = (
        'user',
        'created_at',
        'updated_at',
        'amount',
        'status',
        'return_url',
    )
    date_hierarchy = 'created_at'


def _register(model, admin_class):
    admin.site.register(model, admin_class)


_register(models.Transaction, TransactionAdmin)
