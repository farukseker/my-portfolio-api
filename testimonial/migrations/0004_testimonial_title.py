# Generated by Django 5.1.1 on 2025-01-23 02:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testimonial', '0003_testimonial_linkedin'),
    ]

    operations = [
        migrations.AddField(
            model_name='testimonial',
            name='title',
            field=models.CharField(default='', max_length=75),
            preserve_default=False,
        ),
    ]
