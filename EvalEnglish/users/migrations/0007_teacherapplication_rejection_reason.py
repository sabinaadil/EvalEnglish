# Generated by Django 5.1.4 on 2025-01-16 17:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_alter_teacherapplication_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacherapplication',
            name='rejection_reason',
            field=models.TextField(blank=True, null=True),
        ),
    ]
