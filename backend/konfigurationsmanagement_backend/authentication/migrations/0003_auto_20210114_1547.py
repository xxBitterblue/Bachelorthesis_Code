# Generated by Django 3.1.5 on 2021-01-14 15:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_additionaluserinformation_socket_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='additionaluserinformation',
            name='socket_id',
            field=models.CharField(default='no_socket', max_length=30, verbose_name='socket_id'),
        ),
    ]
