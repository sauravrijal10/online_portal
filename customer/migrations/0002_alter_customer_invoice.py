# Generated by Django 4.2.7 on 2023-12-05 02:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0001_initial'),
        ('customer', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='invoice',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='invoice.invoice'),
        ),
    ]
