# Generated by Django 4.2.7 on 2024-01-22 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('branch', '0003_alter_branch_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='branch',
            name='cr',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='branch',
            name='logo',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='branch',
            name='telephone',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='branch',
            name='website',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]