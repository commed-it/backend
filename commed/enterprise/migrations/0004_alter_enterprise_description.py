# Generated by Django 3.2.8 on 2021-12-13 22:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('enterprise', '0003_alter_enterprise_nif'),
    ]

    operations = [
        migrations.AlterField(
            model_name='enterprise',
            name='description',
            field=models.TextField(default='', help_text='Description about the entity. It can be provided HTML'),
        ),
    ]