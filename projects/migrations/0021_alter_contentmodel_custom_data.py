# Generated by Django 5.1.1 on 2025-01-07 16:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0020_contentmodel_custom_data'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contentmodel',
            name='custom_data',
            field=models.JSONField(blank=True, default='{}', null=True),
        ),
    ]
