from django.db import models

# Create your models here.
import datetime

from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator


class Valutazione(models.Model):
    STATUS_CHOICES = (
        ('Vuoto', 'Vuoto'),
        ('Da Valutare', 'Da valutare'),
        ('In fase di valutazione', 'In fase di valutazione'),
        ('Terminato', 'Terminato'),
    )

    nome = models.CharField(max_length=100, primary_key=True)
    anno = models.IntegerField(validators=[MinValueValidator(
        1000), MaxValueValidator(9999)], default=datetime.date.today().year)
    dataCaricamento = models.DateField(
        blank=True, null=True, verbose_name="data di caricamento")
    status = models.CharField(
        max_length=50, choices=STATUS_CHOICES, default='Vuoto')
    numeroPubblicazioni = models.PositiveIntegerField(
        validators=[MinValueValidator(1)], default=3, verbose_name="numero di pubblicazioni da selezionare")

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name_plural = "Valutazioni"


class Docente(models.Model):
    # Il codice fiscale deve seguire il formato ccccccnncnncnnnc (RSSMRA80L05F593A)
    codiceFiscale = models.CharField(max_length=16, validators=[RegexValidator(
        regex=r'^[a-zA-Z]{6}\d{2}[a-zA-Z]{1}\d{2}[a-zA-Z]{1}\d{3}[a-zA-Z]{1}$')], primary_key=True, default='RSSMRA80L05F593A', verbose_name="codice fiscale")
    cognome_nome = models.CharField(
        max_length=40, verbose_name="cognome e nome")

    def __str__(self):
        return self.cognome_nome.upper()

    class Meta:
        verbose_name_plural = "Docenti"


class RivistaEccellente(models.Model):
    isbn = models.CharField(max_length=30, primary_key=True)
    nome = models.CharField(max_length=60)

    def __str__(self):
        return '{} - {}'.format(self.isbn, self.nome)

    class Meta:
        verbose_name_plural = "Riviste Eccellenti"


class PubblicazionePresentata(models.Model):
    handle = models.CharField(max_length=30, primary_key=True)
    valutazione = models.ForeignKey(
        Valutazione, on_delete=models.CASCADE, null=True, blank=True)
    issn_isbn = models.CharField(
        max_length=30, null=True, blank=True, verbose_name="issn o isbn")
    anno_pubblicazione = models.IntegerField(validators=[MinValueValidator(1000), MaxValueValidator(
        9999)], default=datetime.date.today().year, verbose_name="anno di pubblicazione")
    doi = models.CharField(max_length=30, null=True, blank=True)
    titolo = models.CharField(max_length=200)
    tipologia_collezione = models.CharField(
        max_length=100, verbose_name="tipologia della collezione")
    titolo_rivista_atti = models.CharField(
        max_length=200, null=True, verbose_name="titolo della rivista o atti")
    indicizzato_scopus = models.BooleanField(default=False)
    miglior_quartile = models.IntegerField(blank=True, null=True, validators=[
                                           MinValueValidator(1), MaxValueValidator(4)], verbose_name="miglior quartile")
    num_coautori_dip = models.PositiveIntegerField(
        default=1, validators=[MinValueValidator(1)], verbose_name="numero di coautori del dipartimento")

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=['handle', 'valutazione'], name='chiaveComposta')]

    def __str__(self):
        return self.titolo

    class Meta:
        verbose_name_plural = "Pubblicazioni Presentate"


class RelazioneDocentePubblicazione(models.Model):
    pubblicazione = models.ForeignKey(
        PubblicazionePresentata, on_delete=models.CASCADE)
    autore = models.ForeignKey(Docente, on_delete=models.CASCADE)
    scelta = models.IntegerField(null=True, blank=True, default=0)

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=['pubblicazione', 'autore'], name='chiavePrimariaComposta')]

    def __str__(self):
        return self.pubblicazione.titolo

    class Meta:
        verbose_name_plural = "Relazioni Docente-Pubblicazione"
