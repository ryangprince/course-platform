# Generated by Django 5.1.8 on 2025-04-12 20:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0006_alter_lesson_options_lesson_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='lesson',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
