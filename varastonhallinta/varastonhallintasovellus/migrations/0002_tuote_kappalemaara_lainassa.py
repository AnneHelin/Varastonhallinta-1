# Generated by Django 4.0.3 on 2022-05-05 10:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('varastonhallintasovellus', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tuote',
            name='kappalemaara_lainassa',
            field=models.PositiveIntegerField(default=0, verbose_name='kpl lainassa'),
        ),
    ]