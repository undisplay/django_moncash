# Generated by Django 4.2 on 2023-04-12 13:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('django_moncash', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='moncash_transaction', to=settings.AUTH_USER_MODEL),
        ),
    ]
