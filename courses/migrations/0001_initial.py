# Generated by Django 5.1.6 on 2025-02-18 14:26

import courses.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=120)),
                ('description', models.TextField(blank=True, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to=courses.models.handle_uploaded_file)),
                ('access', models.CharField(choices=[('any', 'Anyone'), ('email', 'Email Required')], default='any', max_length=10)),
                ('status', models.CharField(choices=[('PENDING', 'Pending'), ('PUBLISHED', 'Published'), ('soon', 'Comming Soon'), ('DRAFT', 'Draft')], default='DRAFT', max_length=10)),
            ],
        ),
    ]
