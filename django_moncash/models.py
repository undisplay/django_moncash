from django.db import models

from django.contrib.auth import get_user_model 

import uuid

from django.utils.translation import gettext_lazy as _

User = get_user_model()

class Transaction(models.Model):

    class Status(models.TextChoices):
        PENDING = 'PENDING', _("Pending")
        COMPLETE = 'COMPLETE', _("Complete")
        CONSUME = 'CONSUME', _("Consume")


    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='moncash_transaction'
    )

    order_id = models.CharField(_("Order id"), max_length=50,default=uuid.uuid4,unique=True, editable=False)
    transaction_id = models.CharField(_("Transaction id"), max_length=14,blank=True,null=True,editable=False)
    amount   = models.DecimalField(_("Amount"), max_digits=11, decimal_places=2,blank=False,null=False)
    status = models.CharField(_('Status'),max_length=25,choices=Status.choices,default=Status.PENDING,blank=False)

    return_url = models.TextField(_("Return URL"),blank=False,null=False)

    meta_data = models.JSONField(_("Meta data"),null=True,blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)