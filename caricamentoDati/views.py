import csv, datetime
from django.db import transaction

from django.shortcuts import render, redirect

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


def caricamento(request):
    context = {'valutazioni': Valutazione.objects.all().order_by('anno')}
    return render(request, "caricamentoDati/caricamento.html", context)


def caricamento_con_file(request, filename, valutazione):
    if request.method == 'POST':
        csv_file = request.FILES.get('filename')
        valutazione_nome = request.POST.get('valutazione')
        valutazione = Valutazione.objects.get(nome=valutazione_nome)
        elenco = []
        intestazione = ['anno_di_pubblicazione', 'autore', 'codice_fiscale', 'handle', 'doi', 'titolo',
                        'tipologia_collezione',
                        'issn_o_isbn', 'titolo_rivista_o_atti', 'indicizzato_scopus', 'miglior_quartile_scopus',
                        'num_coautori_interni_dip', 'codice_fiscale']
        riferimento = []
        if csv_file:
            csv_data = csv.reader(csv_file.read().decode(
                'utf-8').splitlines(), delimiter=',')
            for valore in csv_data:
                elenco.append(valore)

            for element in elenco[5]:
                for titolo in intestazione:
                    if element.lower() == titolo:
                        riferimento.append(intestazione.index(titolo))

            n = 100
            with transaction.atomic():
                for riga in elenco[6:]:
                    anno_pubblicazione = riga[0]
                    autore = riga[1]
                    handle = riga[2]
                    doi = riga[3]
                    titolo = riga[4]
                    tipologia_collezione = riga[5]
                    issn_isbn = riga[6]
                    titolo_rivista_atti = riga[7]
                    indicizzato_scopus = riga[8]
                    if riga[9] == '':
                        miglior_quartile = None
                    else:
                        miglior_quartile = int(riga[9])
                    num_coautori_dip = riga[10]
                    codice_fiscale = riga[11]
                    autore=autore.upper()
                    codice_fiscale=codice_fiscale.upper()

                    if not Docente.objects.filter(codiceFiscale=codice_fiscale).exists():
                        Docente(codiceFiscale=codice_fiscale,
                                cognome_nome=autore).save()
                        n = n + 1

                    if not PubblicazionePresentata.objects.filter(handle=handle).exists():
                        PubblicazionePresentata(handle=handle,
                                                issn_isbn=issn_isbn,
                                                anno_pubblicazione=anno_pubblicazione,
                                                doi=doi,
                                                titolo=titolo,
                                                tipologia_collezione=tipologia_collezione,
                                                titolo_rivista_atti=titolo_rivista_atti,
                                                indicizzato_scopus=indicizzato_scopus,
                                                miglior_quartile=miglior_quartile,
                                                num_coautori_dip=num_coautori_dip,
                                                valutazione=valutazione).save()

                    if not RelazioneDocentePubblicazione.objects.filter(pubblicazione=handle,
                                                                        autore__codiceFiscale=codice_fiscale).exists():
                        RelazioneDocentePubblicazione(pubblicazione=PubblicazionePresentata.objects.get(handle=handle),
                                                      autore=Docente.objects.get(codiceFiscale=codice_fiscale)).save()
        
        valutazione.status = "Da Valutare"
        valutazione.save()

    return redirect('valutazioni')


def crea_valutazione(request):
    if request.method == "POST":
        nome = request.POST.get("nome")
        anno = request.POST.get("anno")

        nuova_valutazione = Valutazione(
            nome=nome, anno=anno, dataCaricamento=datetime.date.today(), status = "vuoto")
        nuova_valutazione.save()

    return redirect('caricamento')
