# Generated by Django 5.1.4 on 2025-01-16 10:50

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_remove_teacherapplication_document_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='teacherapplication',
            options={},
        ),
        migrations.RemoveField(
            model_name='teacherapplication',
            name='document',
        ),
        migrations.AddField(
            model_name='teacherapplication',
            name='full_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='teacherapplication',
            name='phone',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='teacherapplication',
            name='submitted_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='teacherapplication',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='teacher_application', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('student', 'Student'), ('teacher', 'Teacher')], default='student', max_length=10),
        ),
    ]
