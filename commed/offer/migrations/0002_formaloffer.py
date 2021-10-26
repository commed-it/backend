# Generated by Django 3.2.8 on 2021-10-26 15:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('offer', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FormalOffer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('version', models.IntegerField()),
                ('contract', models.TextField()),
                ('signedPdf', models.FileField(upload_to='')),
                ('encounterId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='encounterId', to='offer.encounter')),
            ],
        ),
    ]
