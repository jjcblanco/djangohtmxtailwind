# Generated by Django 5.1.6 on 2025-03-05 12:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0006_remove_course_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='public_id',
            field=models.CharField(blank=True, max_length=130, null=True),
        ),
    ]
