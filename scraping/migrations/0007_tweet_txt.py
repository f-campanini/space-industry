# Generated by Django 3.1.7 on 2021-03-28 17:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scraping', '0006_auto_20210328_1738'),
    ]

    operations = [
        migrations.AddField(
            model_name='tweet',
            name='txt',
            field=models.TextField(default=''),
        ),
    ]