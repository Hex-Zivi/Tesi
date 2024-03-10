# Generated by Django 3.2.12 on 2024-03-10 20:49

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('caricamentoDati', '0004_auto_20240310_1653'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='valutazione',
            name='valore',
        ),
        migrations.AddField(
            model_name='valutazione',
            name='numeroPubblicazioni',
            field=models.PositiveIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)], verbose_name='numero di pubblicazioni da selezionare'),
        ),
        migrations.AlterField(
            model_name='valutazione',
            name='status',
            field=models.CharField(choices=[('vuoto', 'Vuoto'), ('da_valutare', 'Da valutare'), ('in_fase_di_valutazione', 'In fase di valutazione'), ('terminato', 'Terminato')], default='', max_length=50),
        ),
    ]
