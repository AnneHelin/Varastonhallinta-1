# Generated by Django 4.0.3 on 2022-05-03 06:01

import datetime
from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Henkilo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(default=None, max_length=254, verbose_name='sähköpostiosoite')),
                ('rooli', models.CharField(choices=[('oppilas', 'Oppilas'), ('varastonhoitaja', 'Varastonhoitaja'), ('opettaja', 'Opettaja'), ('hallinto', 'Hallinto')], default='oppilas', max_length=20)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
                ('vastuuopettaja', models.ForeignKey(blank=True, limit_choices_to=models.Q(('rooli__icontains', 'opettaja')), null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Tuote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('viivakoodi', models.CharField(max_length=30)),
                ('nimike', models.CharField(max_length=100)),
                ('valmistaja', models.CharField(blank=True, max_length=100, null=True)),
                ('kappalemaara', models.PositiveIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)], verbose_name='kappalemäärä')),
                ('tuotekuva', models.ImageField(blank=True, default='default.png', null=True, upload_to='tuotekuvat')),
                ('hankintapaikka', models.CharField(blank=True, max_length=100, null=True)),
                ('hankintapaiva', models.DateField(blank=True, null=True, verbose_name='hankintapäivä')),
                ('hankintahinta', models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True, validators=[django.core.validators.MinValueValidator(0)])),
                ('laskun_numero', models.IntegerField(blank=True, null=True)),
                ('kustannuspaikka', models.CharField(blank=True, max_length=30, null=True)),
                ('takuuaika', models.DateField(blank=True, null=True, verbose_name='takuun päättymispäivä')),
            ],
            options={
                'verbose_name_plural': 'Tuotteet',
            },
        ),
        migrations.CreateModel(
            name='Tuoteryhma',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nimi', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name_plural': 'Tuoteryhmät',
            },
        ),
        migrations.CreateModel(
            name='Varasto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nimi', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name_plural': 'Varastot',
            },
        ),
        migrations.CreateModel(
            name='Varastotyyppi',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nimi', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name_plural': 'Varastotyypit',
            },
        ),
        migrations.CreateModel(
            name='Varastotapahtuma',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tyyppi', models.CharField(choices=[('lainaus', 'Lainaus'), ('palautus', 'Palautus'), ('poistot', 'Poistot'), ('lisays', 'Lisäys')], max_length=10)),
                ('maara', models.IntegerField(help_text='Lainauksille ja poistoille negatiivinen, lisäyksille ja palautuksille positiivinen', verbose_name='määrä')),
                ('arkistotunnus', models.CharField(max_length=50)),
                ('aikaleima', models.DateField(default=datetime.date.today)),
                ('asiakas', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='asiakas', to=settings.AUTH_USER_MODEL)),
                ('tuote', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='varastonhallintasovellus.tuote')),
                ('varasto', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='varastonhallintasovellus.varasto')),
                ('varastonhoitaja', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='varastonhoitaja', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Varastotapahtumat',
            },
        ),
        migrations.AddField(
            model_name='varasto',
            name='varastotyyppi',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='varastonhallintasovellus.varastotyyppi'),
        ),
        migrations.AddField(
            model_name='tuote',
            name='tuoteryhma',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='varastonhallintasovellus.tuoteryhma'),
        ),
        migrations.CreateModel(
            name='Lainaus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('palautuspaiva', models.DateField(help_text='Päivä jona tuote tulisi viimeistään palauttaa', verbose_name='palautuspäivä')),
                ('lainaaja', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL)),
                ('lainaustapahtuma', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='varastonhallintasovellus.varastotapahtuma')),
                ('tuote', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='varastonhallintasovellus.tuote')),
            ],
        ),
    ]
