# Generated by Django 5.1.8 on 2025-04-12 21:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0008_alter_lesson_options_course_timestamp_course_updated_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='public_id',
            field=models.CharField(blank=True, max_length=130, null=True),
        ),
    ]
