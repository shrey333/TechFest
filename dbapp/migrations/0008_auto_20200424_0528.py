# Generated by Django 3.0.3 on 2020-04-23 23:58

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('dbapp', '0007_auto_20200424_0520'),
    ]

    operations = [
        migrations.AlterField(
            model_name='participant',
            name='mobile',
            field=models.BigIntegerField(),
        ),
    ]
