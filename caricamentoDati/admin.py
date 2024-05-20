from django.contrib import admin

# Register your models here.
from . import models


class ValutazioneAdmin(admin.ModelAdmin):
    list_display = ['nome', 'anno', 'status', 'dataCaricamento']


class DocenteAdmin(admin.ModelAdmin):
    list_display = ['cognome_nome', 'codiceFiscale']
    list_filter=["cognome_nome", "codiceFiscale"]
    search_fields=["cognome_nome", "codiceFiscale"]

class PubblicazionePresentataAdmin(admin.ModelAdmin):
    list_display = ['titolo', 'valutazione', 'miglior_quartile', 'num_coautori_dip']
    list_filter=["titolo", "valutazione"]
    search_fields=["titolo"]

class RelazioneDocentePubblicazioneAdmin(admin.ModelAdmin):
    list_display = ['pubblicazione', 'autore', 'scelta']

admin.site.register(models.Valutazione, ValutazioneAdmin)
admin.site.register(models.Docente, DocenteAdmin)
admin.site.register(models.RivistaEccellente)
admin.site.register(models.PubblicazionePresentata, PubblicazionePresentataAdmin)
admin.site.register(models.RelazioneDocentePubblicazione, RelazioneDocentePubblicazioneAdmin)
