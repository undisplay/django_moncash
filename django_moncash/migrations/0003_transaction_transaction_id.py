# Generated by Django 4.2 on 2024-04-13 22:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django_moncash', '0002_alter_transaction_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='transaction_id',
            field=models.CharField(default=None, editable=False, max_length=14, verbose_name='Transaction id'),
        ),
    ]
