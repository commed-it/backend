# Generated by Django 3.2.8 on 2021-12-13 22:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('enterprise', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='enterprise',
            name='NIF',
            field=models.CharField(max_length=30),
        ),
    ]
