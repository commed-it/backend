# Generated by Django 3.2.8 on 2021-11-23 21:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('enterprise', '0005_auto_20211123_0821'),
    ]

    operations = [
        migrations.AlterField(
            model_name='enterprise',
            name='bannerImage',
            field=models.ImageField(default='banner.jpg', upload_to='images/'),
        ),
        migrations.AlterField(
            model_name='enterprise',
            name='profileImage',
            field=models.ImageField(default='profile.png', upload_to='images/'),
        ),
    ]