# Generated by Django 5.0.4 on 2024-05-22 15:45

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Docente',
            fields=[
                ('codiceFiscale', models.CharField(default='RSSMRA80L05F593A', max_length=16, primary_key=True, serialize=False, verbose_name='codice fiscale')),
                ('cognome_nome', models.CharField(max_length=40, verbose_name='cognome e nome')),
            ],
            options={
                'verbose_name_plural': 'Docenti',
            },
        ),
        migrations.CreateModel(
            name='PubblicazionePresentata',
            fields=[
                ('handle', models.CharField(max_length=30, primary_key=True, serialize=False)),
                ('issn_isbn', models.CharField(blank=True, max_length=30, null=True, verbose_name='issn o isbn')),
                ('anno_pubblicazione', models.IntegerField(default=2024, validators=[django.core.validators.MinValueValidator(1000), django.core.validators.MaxValueValidator(9999)], verbose_name='anno di pubblicazione')),
                ('doi', models.CharField(blank=True, max_length=30, null=True)),
                ('titolo', models.CharField(max_length=200)),
                ('tipologia_collezione', models.CharField(max_length=100, verbose_name='tipologia della collezione')),
                ('titolo_rivista_atti', models.CharField(max_length=200, null=True, verbose_name='titolo della rivista o atti')),
                ('indicizzato_scopus', models.BooleanField(default=False)),
                ('miglior_quartile', models.IntegerField(blank=True, default=0, validators=[django.core.validators.MinValueValidator(0)], verbose_name='miglior quartile')),
                ('num_coautori_dip', models.PositiveIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)], verbose_name='numero di coautori del dipartimento')),
            ],
            options={
                'verbose_name_plural': 'Pubblicazioni Presentate',
            },
        ),
        migrations.CreateModel(
            name='Valutazione',
            fields=[
                ('nome', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('anno', models.IntegerField(default=2024, validators=[django.core.validators.MinValueValidator(1000), django.core.validators.MaxValueValidator(9999)])),
                ('dataCaricamento', models.DateField(blank=True, null=True, verbose_name='data di caricamento')),
                ('status', models.CharField(choices=[('Vuota', 'Vuota'), ('Pubblicazioni caricate', 'Pubblicazioni caricate'), ('Assegnamento calcolato', 'Assegnamento calcolato'), ('Assegnamento completato', 'Assegnamento completato'), ('Chiusa', 'Chiusa')], default='Vuota', max_length=50)),
                ('numeroPubblicazioni', models.PositiveIntegerField(default=3, validators=[django.core.validators.MinValueValidator(1)], verbose_name='numero di pubblicazioni da selezionare')),
                ('dataCaricamentoPubblicazioni', models.DateField(blank=True, null=True, verbose_name='data di caricamento delle pubblicazioni')),
            ],
            options={
                'verbose_name_plural': 'Valutazioni',
            },
        ),
        migrations.CreateModel(
            name='RelazioneDocentePubblicazione',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('scelta', models.IntegerField(blank=True, default=0, null=True)),
                ('autore', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='caricamentoDati.docente')),
                ('pubblicazione', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='caricamentoDati.pubblicazionepresentata')),
            ],
            options={
                'verbose_name_plural': 'Relazioni Docente-Pubblicazione',
            },
        ),
        migrations.CreateModel(
            name='RivistaEccellente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('isbn', models.CharField(blank=True, max_length=30, null=True)),
                ('nome', models.CharField(max_length=60)),
                ('link', models.CharField(default='_', max_length=200)),
                ('valutazione', models.ForeignKey(default='_', on_delete=django.db.models.deletion.CASCADE, to='caricamentoDati.valutazione')),
            ],
            options={
                'verbose_name_plural': 'Riviste Eccellenti',
            },
        ),
        migrations.AddField(
            model_name='pubblicazionepresentata',
            name='valutazione',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='caricamentoDati.valutazione'),
        ),
    ]
