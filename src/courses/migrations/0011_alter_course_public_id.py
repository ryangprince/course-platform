# Generated by Django 5.1.8 on 2025-04-17 18:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0010_lesson_public_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='public_id',
            field=models.CharField(blank=True, db_index=True, max_length=130, null=True),
        ),
    ]
