# Generated by Django 5.0.6 on 2024-05-20 04:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='studentpayment',
            name='hostel_fee_due',
        ),
        migrations.RemoveField(
            model_name='studentpayment',
            name='hostel_fee_paid',
        ),
        migrations.RemoveField(
            model_name='studentpayment',
            name='hostel_fee_total',
        ),
    ]
