# Generated by Django 3.0.3 on 2020-04-23 23:50

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('dbapp', '0005_newsletter'),
    ]

    operations = [
        migrations.AlterField(
            model_name='participant',
            name='mobile',
            field=models.IntegerField(max_length=15),
        ),
    ]
