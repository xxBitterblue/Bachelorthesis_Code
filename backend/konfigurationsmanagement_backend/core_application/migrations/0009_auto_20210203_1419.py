# Generated by Django 3.1.5 on 2021-02-03 14:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core_application', '0008_auto_20210202_1928'),
    ]

    operations = [
        migrations.AlterField(
            model_name='changehistoryentry',
            name='changes',
            field=models.JSONField(blank=True, null=True),
        ),
    ]
