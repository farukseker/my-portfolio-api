# Generated by Django 5.0.3 on 2024-09-12 07:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('analytical', '0007_analyticmedia_created_at_analyticmedia_updated_at'),
    ]

    operations = [
        migrations.RenameField(
            model_name='analyticmedia',
            old_name='platform_path',
            new_name='platform_href',
        ),
    ]
