# Generated by Django 3.0.3 on 2020-03-13 13:20

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('dbapp', '0004_auto_20200307_2046'),
    ]

    operations = [
        migrations.CreateModel(
            name='Newsletter',
            fields=[
                ('email', models.EmailField(max_length=254, primary_key=True, serialize=False)),
            ],
        ),
    ]