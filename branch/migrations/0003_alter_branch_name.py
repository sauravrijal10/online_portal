# Generated by Django 4.2.7 on 2024-01-11 16:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('branch', '0002_branch_city'),
    ]

    operations = [
        migrations.AlterField(
            model_name='branch',
            name='name',
            field=models.CharField(max_length=251),
        ),
    ]
