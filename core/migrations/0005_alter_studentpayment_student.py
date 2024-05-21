# Generated by Django 5.0.6 on 2024-05-20 17:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_alter_studentpayment_student'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentpayment',
            name='student',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='payments', to='core.student'),
        ),
    ]