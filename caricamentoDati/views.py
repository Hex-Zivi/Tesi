from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

from .models import *
from django.shortcuts import render


def valutazioni(request):
    context = {'valutazioni': Valutazione.objects.all().order_by('anno')}
    return render(request, "caricamentoDati/valutazioni.html", context)


def valutazione(request, pk):
    try:
        valutazione = Valutazione.objects.get(pk=pk)
        return HttpResponse(f'"{valutazione.nome}" caricata il {valutazione.dataCaricamento}, {valutazione.status}<br>')
    except Valutazione.DoesNotExist:
        return HttpResponse(f'Valutazione chiamata "{pk}" inesistente')


def valutazione_per_anno(request, mese, anno):
    valutazioni = Valutazione.objects.filter(dataCaricamento__year=int(anno))
    valutazioni = valutazioni.filter(dataCaricamento__month=int(mese))
    elenco = ""
    for valutazione in valutazioni.order_by("anno"):
        elenco += (f'"{valutazione.nome}" caricata il {valutazione.dataCaricamento}, {valutazione.status}<br>')
    return HttpResponse(elenco)
