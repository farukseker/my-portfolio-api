# Generated by Django 5.0.3 on 2024-09-12 01:33

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0008_alter_surveyuser_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='surveyuser',
            name='token',
            field=models.UUIDField(default=uuid.UUID('700845a9-3d45-4489-bfff-4042aebd236f')),
        ),
    ]
