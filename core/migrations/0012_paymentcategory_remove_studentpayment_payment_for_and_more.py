# Generated by Django 5.0.4 on 2024-05-07 15:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_alter_expense_amount_alter_studentpayment_due_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
            ],
        ),
        migrations.RemoveField(
            model_name='studentpayment',
            name='payment_for',
        ),
        migrations.AddField(
            model_name='studentpayment',
            name='payment_for',
            field=models.ManyToManyField(to='core.paymentcategory'),
        ),
    ]
