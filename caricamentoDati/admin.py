from django.contrib import admin

# Register your models here.
from . import models


class ValutazioneAdmin(admin.ModelAdmin):
    list_display = ['nome', 'anno', 'dataCaricamento']


class DocenteAdmin(admin.ModelAdmin):
    list_display = ['cognome_nome', 'codiceFiscale']


admin.site.register(models.Valutazione, ValutazioneAdmin)
admin.site.register(models.Docente, DocenteAdmin)
admin.site.register(models.RivistaEccellente)
admin.site.register(models.PubblicazionePresentata)
admin.site.register(models.RelazioneDocentePubblicazione)
