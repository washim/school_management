# Generated by Django 5.0.6 on 2024-05-21 07:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_alter_studentpayment_student'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expense',
            name='created',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='expense',
            name='updated',
            field=models.DateField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='studentpayment',
            name='created',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='studentpayment',
            name='updated',
            field=models.DateField(auto_now=True),
        ),
    ]
