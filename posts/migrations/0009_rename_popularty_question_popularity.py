# Generated by Django 5.0.1 on 2024-04-15 01:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0008_topic_address_topic_topic_date'),
    ]

    operations = [
        migrations.RenameField(
            model_name='question',
            old_name='popularty',
            new_name='popularity',
        ),
    ]
