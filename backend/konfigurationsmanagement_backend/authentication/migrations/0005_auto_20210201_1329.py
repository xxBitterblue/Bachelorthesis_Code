# Generated by Django 3.1.5 on 2021-02-01 13:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0004_auto_20210115_1422'),
    ]

    operations = [
        migrations.AlterField(
            model_name='additionaluserinformation',
            name='role',
            field=models.CharField(choices=[('USER', 'User'), ('ADMIN', 'Admin')], default='USER', max_length=30),
        ),
    ]
