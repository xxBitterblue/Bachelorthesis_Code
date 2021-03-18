# Generated by Django 3.1.5 on 2021-01-15 14:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0003_auto_20210114_1547'),
    ]

    operations = [
        migrations.AlterField(
            model_name='additionaluserinformation',
            name='role',
            field=models.CharField(choices=[('USER', 'User'), ('ADMIN', 'Admin'), ('ENTERER', 'Enterer')], default='USER', max_length=30),
        ),
    ]