# Generated by Django 5.0.6 on 2024-05-12 13:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0022_alter_studentpayment_admission_fee_due_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='studentpayment',
            name='payment_date',
        ),
    ]
