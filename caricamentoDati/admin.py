from django.contrib import admin
from . import models
from .models import CustomUser

class ValutazioneAdmin(admin.ModelAdmin):
    list_display = ['nome', 'anno', 'status', 'dataCaricamento']

class DocenteAdmin(admin.ModelAdmin):
    list_display = ['cognome_nome', 'codiceFiscale']
    search_fields = ["cognome_nome", "codiceFiscale"]

class PubblicazionePresentataAdmin(admin.ModelAdmin):
    list_display = ['short_titolo', 'valutazione', 'miglior_quartile', 'num_coautori_dip']
    list_filter = ["valutazione"]
    search_fields = ["titolo"]

    def short_titolo(self, obj):
        return (obj.titolo[:40] + '...') if len(obj.titolo) > 30 else obj.titolo

    short_titolo.short_description = 'Titolo'

class RelazioneDocentePubblicazioneAdmin(admin.ModelAdmin):
    list_display = ['short_pubblicazione', 'autore', 'scelta']
    list_filter = ["pubblicazione__valutazione", "scelta"]
    search_fields = ["autore__cognome_nome", "pubblicazione__titolo"]

    def short_pubblicazione(self, obj):
        return (obj.pubblicazione.titolo[:40] + '...') if len(obj.pubblicazione.titolo) > 30 else obj.pubblicazione.titolo

    short_pubblicazione.short_description = 'Pubblicazione'

class RivistaEccellenteAdmin(admin.ModelAdmin):
    list_display = ['nome', 'issn1', 'issn2', 'valutazione']
    list_filter = ["valutazione"]

admin.site.register(models.Valutazione, ValutazioneAdmin)
admin.site.register(models.Docente, DocenteAdmin)
admin.site.register(models.RivistaEccellente, RivistaEccellenteAdmin)
admin.site.register(models.PubblicazionePresentata, PubblicazionePresentataAdmin)
admin.site.register(models.RelazioneDocentePubblicazione, RelazioneDocentePubblicazioneAdmin)
admin.site.register(CustomUser)
