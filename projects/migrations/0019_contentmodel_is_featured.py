# Generated by Django 5.1.1 on 2024-12-28 15:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0018_alter_contenttypemodel_sub_tags'),
    ]

    operations = [
        migrations.AddField(
            model_name='contentmodel',
            name='is_featured',
            field=models.BooleanField(default=False),
        ),
    ]
