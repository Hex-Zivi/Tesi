# forms.py

from django import forms
from django.forms.widgets import CheckboxSelectMultiple
from .models import *


class FormCreaValutazione(forms.ModelForm):
    class Meta:
        model = Valutazione
        fields = ['nome', 'anno', 'numeroPubblicazioni']


class FormAggiungiPubblicazione(forms.ModelForm):
    autori = forms.ModelMultipleChoiceField(queryset=Docente.objects.all().order_by(
        'cognome_nome'), required=False, widget=CheckboxSelectMultiple)

    class Meta:
        model = PubblicazionePresentata
        fields = ['handle', 'titolo', 'anno_pubblicazione', 'miglior_quartile', 'issn_isbn',
                  'doi', 'tipologia_collezione', 'titolo_rivista_atti', 'indicizzato_scopus']
