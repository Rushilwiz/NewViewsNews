# Generated by Django 3.1 on 2020-08-15 15:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0003_auto_20200815_1130'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='headline',
            field=models.TextField(default='Headline'),
            preserve_default=False,
        ),
    ]