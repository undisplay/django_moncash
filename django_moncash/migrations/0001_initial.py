# Generated by Django 4.2 on 2023-04-07 15:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.CharField(default=uuid.uuid4, editable=False, max_length=50, unique=True, verbose_name='Order id')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=11, verbose_name='Amount')),
                ('status', models.CharField(choices=[('PENDING', 'Pending'), ('COMPLETE', 'Complete'), ('CONSUME', 'Consume')], default='PENDING', max_length=25, verbose_name='Status')),
                ('return_url', models.TextField(verbose_name='Return URL')),
                ('meta_data', models.JSONField(blank=True, null=True, verbose_name='Meta data')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]