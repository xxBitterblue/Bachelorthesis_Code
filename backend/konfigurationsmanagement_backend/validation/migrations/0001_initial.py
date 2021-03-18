# Generated by Django 3.1.5 on 2021-02-05 13:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core_application', '0010_requirementgroup_requirement_group_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ValidationRule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('active', models.BooleanField(default=True)),
                ('is_global', models.BooleanField(default=True)),
                ('rule', models.TextField()),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('categorys', models.ManyToManyField(to='core_application.Category')),
            ],
        ),
    ]