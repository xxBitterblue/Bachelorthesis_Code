# Generated by Django 3.1.5 on 2021-02-22 19:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('software', '0002_auto_20210118_1603'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImmutableSoftware',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('software.software',),
        ),
    ]
