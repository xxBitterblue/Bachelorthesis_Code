# Generated by Django 3.1.5 on 2021-02-22 19:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('authentication', '0005_auto_20210201_1329'),
    ]

    operations = [
        migrations.CreateModel(
            name='DashboardEntry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_id', models.IntegerField()),
                ('message', models.TextField()),
                ('timestamp', models.DateField()),
                ('editor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='additionaluserinformation',
            name='dashboard',
            field=models.ManyToManyField(to='authentication.DashboardEntry'),
        ),
    ]
