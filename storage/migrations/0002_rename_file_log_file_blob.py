# Generated by Django 4.2.1 on 2023-05-16 09:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('storage', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='log',
            old_name='file',
            new_name='file_blob',
        ),
    ]
