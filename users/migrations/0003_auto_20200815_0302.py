# Generated by Django 3.1 on 2020-08-15 07:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20200815_0300'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='pfp',
            new_name='profile_pic',
        ),
    ]
