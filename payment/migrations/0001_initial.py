# Generated by Django 4.2.7 on 2023-12-05 11:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('invoice', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.BigIntegerField()),
                ('payment_status', models.CharField(choices=[('COMPLETED', 'Completed'), ('INCOMPLETE', 'Incomplete')], max_length=50)),
                ('payment_source', models.CharField(choices=[('CASH', 'Cash'), ('BANK_TRANSFER', 'Bank_Transfer'), ('CHEQUE', 'Cheque')], max_length=50)),
                ('bank_name', models.CharField(max_length=255)),
                ('cheque_number', models.CharField(max_length=255)),
                ('payment_description', models.CharField(max_length=1000)),
                ('payment_type', models.CharField(choices=[('FIRST', 'First'), ('SECOND', 'Second'), ('THIRD', 'Third')], max_length=50)),
                ('remark', models.CharField(max_length=1000)),
                ('invoice_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='invoice.invoice')),
                ('payment_creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
