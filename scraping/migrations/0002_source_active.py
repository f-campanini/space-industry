# Generated by Django 3.1.7 on 2021-03-03 20:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scraping', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='source',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]
