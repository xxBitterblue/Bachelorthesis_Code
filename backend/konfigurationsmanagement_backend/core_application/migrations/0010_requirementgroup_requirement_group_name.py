# Generated by Django 3.1.5 on 2021-02-03 19:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core_application', '0009_auto_20210203_1419'),
    ]

    operations = [
        migrations.AddField(
            model_name='requirementgroup',
            name='requirement_group_name',
            field=models.CharField(default='Anfordrungsgruppe', max_length=30),
        ),
    ]