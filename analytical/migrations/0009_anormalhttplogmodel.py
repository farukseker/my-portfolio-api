# Generated by Django 5.1.1 on 2024-12-27 07:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analytical', '0008_rename_platform_path_analyticmedia_platform_href'),
    ]

    operations = [
        migrations.CreateModel(
            name='ANormalHttpLogModel',
            fields=[
                ('viewmodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='analytical.viewmodel')),
            ],
            bases=('analytical.viewmodel',),
        ),
    ]
