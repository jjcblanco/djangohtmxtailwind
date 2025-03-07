# Generated by Django 5.1.6 on 2025-03-07 13:29

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0008_lesson_public_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lesson',
            name='thumbnail',
            field=cloudinary.models.CloudinaryField(blank=True, max_length=255, null=True, verbose_name='image'),
        ),
    ]
