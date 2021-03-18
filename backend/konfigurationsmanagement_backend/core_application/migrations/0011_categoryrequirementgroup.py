# Generated by Django 3.1.5 on 2021-02-08 12:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core_application', '0010_requirementgroup_requirement_group_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='CategoryRequirementGroup',
            fields=[
                ('requirementgroup_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core_application.requirementgroup')),
                ('reference_groups', models.ManyToManyField(related_name='categoryrequirementgroup_groups', to='core_application.RequirementGroup')),
            ],
            bases=('core_application.requirementgroup',),
        ),
    ]