# Generated by Django 5.1.6 on 2025-02-25 15:09

import cloudinary.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0003_lesson'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='lesson',
            options={'ordering': ['order']},
        ),
        migrations.RemoveField(
            model_name='lesson',
            name='video_url',
        ),
        migrations.AddField(
            model_name='lesson',
            name='order',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='lesson',
            name='video',
            field=cloudinary.models.CloudinaryField(max_length=255, null=True, verbose_name='video'),
        ),
    ]
