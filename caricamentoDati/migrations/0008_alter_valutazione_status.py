# Generated by Django 3.2.12 on 2024-03-11 08:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('caricamentoDati', '0007_valutazione_datacaricamentopubblicazioni'),
    ]

    operations = [
        migrations.AlterField(
            model_name='valutazione',
            name='status',
            field=models.CharField(choices=[('Vuota', 'Vuota'), ('Pubblicazioni Caricate', 'Pubblicazioni caricate'), ('Assegnamento calcolato', 'Assegnamento calcolato'), ('Assegnamento completato', 'Assegnamento completato'), ('Chiusa', 'Chiusa')], default='Vuota', max_length=50),
        ),
    ]
