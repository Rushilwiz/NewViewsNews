# Generated by Django 3.1 on 2020-08-15 23:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_profile_tag'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='tag',
        ),
    ]