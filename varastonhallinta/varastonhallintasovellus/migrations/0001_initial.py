# Generated by Django 4.0.3 on 2022-04-05 10:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Henkilo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(default=None, max_length=254)),
                ('etunimi', models.CharField(max_length=20)),
                ('sukunimi', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Rooli',
            fields=[
                ('roolinimitys', models.CharField(max_length=20, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Tuote',
            fields=[
                ('viivakoodi', models.CharField(max_length=30, primary_key=True, serialize=False)),
                ('tuote_id', models.IntegerField()),
                ('nimike', models.CharField(max_length=50)),
                ('kappalemaara', models.IntegerField()),
                ('tuotekuva', models.ImageField(blank=True, null=True, upload_to=None)),
                ('hankintapaikka', models.CharField(blank=True, max_length=50, null=True)),
                ('hankintavuosi', models.IntegerField(blank=True, null=True)),
                ('hankintahinta', models.FloatField(blank=True, null=True)),
                ('laskun_numero', models.IntegerField(blank=True, null=True)),
                ('kustannuspaikka', models.CharField(blank=True, max_length=10, null=True)),
                ('takuuaika', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Tuoteryhma',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ryhman_nimi', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Varasto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('varaston_nimi', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Varastotyyppi',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('varastotyypin_nimi', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Varastotapahtuma',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('palautuspaiva', models.DateTimeField()),
                ('maara', models.IntegerField(default=1)),
                ('arkistotunnus', models.CharField(max_length=50)),
                ('aikaleima', models.DateTimeField()),
                ('asiakas_FK', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='asiakas', to='varastonhallintasovellus.henkilo')),
                ('varasto_FK', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='varastofk', to='varastonhallintasovellus.varasto')),
                ('varastonhoitaja_FK', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='varastonhoitaja', to='varastonhallintasovellus.henkilo')),
                ('viivakoodi_FK', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='varastonhallintasovellus.tuote')),
            ],
        ),
        migrations.AddField(
            model_name='varasto',
            name='varastotyyppi_FK',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='varastonhallintasovellus.varastotyyppi'),
        ),
        migrations.AddField(
            model_name='tuote',
            name='varaston_nimi',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='tuotesijainti', to='varastonhallintasovellus.varasto'),
        ),
        migrations.AddField(
            model_name='henkilo',
            name='roolinimitys_FK',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='varastonhallintasovellus.rooli'),
        ),
    ]
