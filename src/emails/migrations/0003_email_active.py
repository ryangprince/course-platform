# Generated by Django 5.1.8 on 2025-04-18 21:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emails', '0002_rename_emailverification_emailverificationevent'),
    ]

    operations = [
        migrations.AddField(
            model_name='email',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]
