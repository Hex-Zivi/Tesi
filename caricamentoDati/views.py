import csv
import datetime
from django.db import transaction

from django.shortcuts import render, redirect

# Create your views here.
from django.http import HttpResponse

from .models import *
from django.db.models import Count
from django.shortcuts import render


from pdb import set_trace


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
        valutazione = Valutazione.objects.get(nome=valutazione)
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
                    indicizzato_scopus = riga[8].lower()
                    if indicizzato_scopus in ['vero', '1', 'true']:
                        indicizzato_scopus = True
                    else:
                        indicizzato_scopus = False
                    if riga[9] == '':
                        miglior_quartile = 0
                    else:
                        miglior_quartile = int(riga[9])
                    num_coautori_dip = riga[10]
                    codice_fiscale = riga[11]
                    autore = autore.upper()
                    codice_fiscale = codice_fiscale.upper()

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

        valutazione.status = "Pubblicazioni caricate"
        valutazione.dataCaricamentoPubblicazioni = datetime.date.today()
        valutazione.save()

    return redirect('modifica_valutazione', valutazione)


def crea_valutazione(request):
    if request.method == "POST":
        nome = request.POST.get("nome")
        anno = request.POST.get("anno")

        nuova_valutazione = Valutazione(
            nome=nome, anno=anno, dataCaricamento=datetime.date.today(), status="Vuota")
        nuova_valutazione.save()

    return redirect('valutazioni')


def cancella_valutazione_(request):
    return redirect('valutazioni')


def cancella_valutazione(request, valutazione_nome):
    valutazioneDaCancellate = Valutazione.objects.filter(nome=valutazione_nome)
    valutazioneDaCancellate.delete()
    return redirect('valutazioni')


def modifica_valutazione_(request):
    return redirect('valutazioni')


def modifica_valutazione(request, valutazione_nome):
    valutazione = Valutazione.objects.get(nome=valutazione_nome)
    context = {'valutazione': valutazione, 'pubblicazioni': PubblicazionePresentata.objects.filter(
        valutazione=valutazione).order_by('titolo')}
    return render(request, 'caricamentoDati/modifica.html', context)


def cancella_pubblicazioni_tot_(request):
    return redirect('modifica_valutazione')


def cancella_pubblicazioni_tot(request, valutazione_nome):
    valutazione = Valutazione.objects.get(nome=valutazione_nome)
    pubblicazioni = PubblicazionePresentata.objects.filter(
        valutazione=valutazione)
    for pubblicazione in pubblicazioni:
        pubblicazione.delete()
    return redirect('modifica_valutazione', valutazione)


def cancella_pubblicazione_singola(request, pubblicazione_titolo, valutazione_nome):
    valutazione = Valutazione.objects.get(nome=valutazione_nome)
    PubblicazionePresentata.objects.get(titolo=pubblicazione_titolo).delete()
    return redirect('modifica_valutazione', valutazione)


def assegnamento(request, valutazione_nome):
    valutazione = Valutazione.objects.get(nome=valutazione_nome)
    relazioni_docente_pubblicazione = RelazioneDocentePubblicazione.objects.filter(
        pubblicazione__valutazione=valutazione)

    docenti_info = []

    for docente in Docente.objects.all().order_by('cognome_nome'):
        num_pubblicazioni_richieste = valutazione.numeroPubblicazioni
        num_pubblicazioni_assegnate = relazioni_docente_pubblicazione.filter(
            autore=docente).exclude(scelta__isnull=True).exclude(scelta=0).count()
        quartili = sorted(set(relazione.pubblicazione.miglior_quartile for relazione in relazioni_docente_pubblicazione.filter(
            autore=docente).exclude(scelta__isnull=True).exclude(scelta=0)), reverse=True)
        pubblicazioni_totali = relazioni_docente_pubblicazione.filter(
            autore=docente).count()
        formatted_quartili = ['Q{}'.format(
            q) if q != 0 else '_' for q in quartili]

        docente_info = {
            'codice_fiscale': docente.codiceFiscale,
            'cognome_nome': docente.cognome_nome,
            'num_pubblicazioni_richieste': num_pubblicazioni_richieste,
            'num_pubblicazioni_assegnate': num_pubblicazioni_assegnate,
            'pubblicazioni_totali': pubblicazioni_totali,
            'quartili': formatted_quartili

        }

        docenti_info.append(docente_info)

    informazioni = {'docenti_info': docenti_info}
    context = {'valutazione': valutazione,
               'informazioni_docente': informazioni}
    return render(request, 'caricamentoDati/assegnamento.html', context)


def docente_pubblicazioni(request, valutazione_nome, docente_codice_fiscale):
    valutazione = Valutazione.objects.get(nome=valutazione_nome)
    docente = Docente.objects.get(codiceFiscale=docente_codice_fiscale)
    relazioni_docente_pubblicazione = RelazioneDocentePubblicazione.objects.filter(
        pubblicazione__valutazione=valutazione, autore=docente)

    pubblicazioni_info = []

    for relazione in relazioni_docente_pubblicazione:
        pubblicazione = relazione.pubblicazione
        altri_autori = [autore.cognome_nome for autore in Docente.objects.filter(
            relazionedocentepubblicazione__pubblicazione=pubblicazione
        ).exclude(codiceFiscale=docente_codice_fiscale).distinct()]
        altri_autori_scelta = [autore.cognome_nome for autore in Docente.objects.filter(
            relazionedocentepubblicazione__pubblicazione=pubblicazione, relazionedocentepubblicazione__scelta__gt=0
        ).exclude(codiceFiscale=docente_codice_fiscale).distinct()]
        valore_scelta = relazione.scelta
        quartile = pubblicazione.miglior_quartile

        pubblicazione_info = {
            'titolo': pubblicazione.titolo,
            'altri_autori': altri_autori,
            'altri_autori_scelta': altri_autori_scelta,
            'valore_scelta': valore_scelta,
            'quartile': quartile
        }

        pubblicazioni_info.append(pubblicazione_info)

    context = {'valutazione': valutazione,
               'docente': docente,
               'docente_codice_fiscale': docente.codiceFiscale,
               'pubblicazioni_info': pubblicazioni_info}
    return render(request, 'caricamentoDati/docente_pubblicazioni.html', context)


# Vista di assegnamento delle pubblicazioni nella valutazione
def calcola_numero_coautori_possibili(pubblicazione, relazioni_docente_pubblicazione, docenti):
    coautori_pubblicazione = set()
    for relazione in relazioni_docente_pubblicazione.filter(pubblicazione=pubblicazione):
        coautori_pubblicazione.add(relazione.autore)
    return len(coautori_pubblicazione.intersection(docenti))


def rimuovi_docente(docente, pubblicazioni, relazioni_docente_pubblicazione, docenti, numero_coautori_possibili_pubblicazione):
    if docente in docenti:
        print("Docente rimosso:", docente)
        relazioni_docente_pubblicazione = relazioni_docente_pubblicazione.exclude(
            autore=docente)
        docenti = docenti.exclude(pk=docente.pk)
        for pubblicazione in pubblicazioni:
            numero_coautori_possibili_pubblicazione[pubblicazione.pk] = calcola_numero_coautori_possibili(
                pubblicazione, relazioni_docente_pubblicazione, docenti)
        print("Numero di relazioni:", len(relazioni_docente_pubblicazione)," Numero di docenti:", len(docenti))
    return docenti, numero_coautori_possibili_pubblicazione, relazioni_docente_pubblicazione


def assegnamento_algoritmo(request, valutazione_nome):
    valutazione = Valutazione.objects.get(nome=valutazione_nome)
    numero_selezioni_valutazione = valutazione.numeroPubblicazioni
    pubblicazioni = PubblicazionePresentata.objects.filter(
        valutazione=valutazione)
    relazioni_docente_pubblicazione = RelazioneDocentePubblicazione.objects.filter(
        pubblicazione__valutazione=valutazione)
    docenti = Docente.objects.annotate(num_relazioni=Count(
        'relazionedocentepubblicazione')).order_by('num_relazioni')

    numero_selezioni_docente = {docente.pk: 0 for docente in docenti}

    numero_coautori_possibili_pubblicazione = {}

    for pubblicazione in pubblicazioni:
        numero_coautori_possibili_pubblicazione[pubblicazione.pk] = calcola_numero_coautori_possibili(
            pubblicazione, relazioni_docente_pubblicazione, docenti)

    progresso = 1
    giro = 0

    while progresso == 1:
        journal_1_singoloAutore = pubblicazioni.filter(
            miglior_quartile__in=[0, 1], num_coautori_dip=1)
        journal_2_singoloAutore = pubblicazioni.filter(
            miglior_quartile=2, num_coautori_dip=1)
        journal_3_singoloAutore = pubblicazioni.filter(
            num_coautori_dip=1).exclude(miglior_quartile__in=[0, 1, 2])

        journal_1 = pubblicazioni.filter(
            miglior_quartile__in=[0, 1]).exclude(num_coautori_dip=1)
        journal_2 = pubblicazioni.filter(
            miglior_quartile=2).exclude(num_coautori_dip=1)
        journal_3 = pubblicazioni.exclude(
            miglior_quartile__in=[0, 1, 2], num_coautori_dip=1)

        progresso = 0
        giro += 1

        # Selezione di pubblicazioni con autore singolo
        for docente in docenti.order_by('cognome_nome'):
            '''set_trace()'''
            '''print("Docente in valutazione:", docente, ", giro:", giro)'''
            for journal in [journal_1_singoloAutore, journal_2_singoloAutore, journal_3_singoloAutore]:
                if docente in docenti:
                    for pubblicazione in journal.filter(relazionedocentepubblicazione__autore=docente):

                        if numero_selezioni_docente.get(docente.pk, 0) == numero_selezioni_valutazione:
                            docenti, numero_coautori_possibili_pubblicazione, relazioni_docente_pubblicazione = rimuovi_docente(
                                docente, pubblicazioni, relazioni_docente_pubblicazione, docenti, numero_coautori_possibili_pubblicazione)
                            break

                        if numero_coautori_possibili_pubblicazione[pubblicazione.pk] == 1 and pubblicazione in pubblicazioni.filter(relazionedocentepubblicazione__autore=docente):
                            relazione = RelazioneDocentePubblicazione.objects.get(
                                pubblicazione=pubblicazione, autore=docente)
                            relazione.scelta = 1
                            relazione.save()

                            progresso = 1

                            numero_selezioni_docente[docente.pk] += 1
                            if numero_selezioni_docente.get(docente.pk, 0) == numero_selezioni_valutazione:
                                docenti, numero_coautori_possibili_pubblicazione, relazioni_docente_pubblicazione = rimuovi_docente(
                                    docente, pubblicazioni, relazioni_docente_pubblicazione, docenti, numero_coautori_possibili_pubblicazione)
                                progresso = 1
                                break

                if numero_selezioni_docente.get(docente.pk, 0) == numero_selezioni_valutazione:
                    docenti, numero_coautori_possibili_pubblicazione, relazioni_docente_pubblicazione = rimuovi_docente(
                        docente, pubblicazioni, relazioni_docente_pubblicazione, docenti, numero_coautori_possibili_pubblicazione)

        # Selezione di pubblicazioni con autori multipli
        if progresso == 0:
            '''set_trace()'''
            for journal in [journal_1, journal_2, journal_3]:
                if docente in docenti:

                    for pubblicazione in journal.filter(relazionedocentepubblicazione__autore=docente):

                        if numero_selezioni_docente.get(docente.pk, 0) == numero_selezioni_valutazione:
                            docenti, numero_coautori_possibili_pubblicazione, relazioni_docente_pubblicazione = rimuovi_docente(
                                docente, pubblicazioni, relazioni_docente_pubblicazione, docenti, numero_coautori_possibili_pubblicazione)
                            break

                        if numero_coautori_possibili_pubblicazione[pubblicazione.pk] == 1 and pubblicazione in pubblicazioni.filter(relazionedocentepubblicazione__autore=docente):
                            relazione = RelazioneDocentePubblicazione.objects.get(
                                pubblicazione=pubblicazione, autore=docente)
                            relazione.scelta = 1
                            relazione.save()

                            progresso = 1

                            numero_selezioni_docente[docente.pk] += 1
                            if numero_selezioni_docente.get(docente.pk, 0) == numero_selezioni_valutazione:
                                docenti, numero_coautori_possibili_pubblicazione, relazioni_docente_pubblicazione = rimuovi_docente(
                                    docente, pubblicazioni, relazioni_docente_pubblicazione, docenti, numero_coautori_possibili_pubblicazione)
                                progresso = 1
                                break

                    if numero_selezioni_docente.get(docente.pk, 0) == numero_selezioni_valutazione:
                        docenti, numero_coautori_possibili_pubblicazione, relazioni_docente_pubblicazione = rimuovi_docente(
                            docente, pubblicazioni, relazioni_docente_pubblicazione, docenti, numero_coautori_possibili_pubblicazione)

    print("LISTA DOCENTI: ")
    for docente in docenti:
        print(docente)

    return redirect('assegnamento', valutazione)


def azzera_assegnamento(request, valutazione_nome):
    valutazione = Valutazione.objects.get(nome=valutazione_nome)
    relazioni_docente_pubblicazione = RelazioneDocentePubblicazione.objects.filter(
        pubblicazione__valutazione=valutazione)

    for relazione in relazioni_docente_pubblicazione:
        relazione.scelta = 0
        relazione.save()

    return redirect('assegnamento', valutazione)


'''def assegnamento_algoritmo(request, valutazione_nome):
    valutazione = Valutazione.objects.get(nome=valutazione_nome)
    numero_selezioni_valutazione = valutazione.numeroPubblicazioni
    pubblicazioni = PubblicazionePresentata.objects.filter(valutazione=valutazione)
    relazioni_docente_pubblicazione = RelazioneDocentePubblicazione.objects.filter(pubblicazione__valutazione=valutazione)
    docenti = Docente.objects.annotate(num_relazioni=Count('relazionedocentepubblicazione')).order_by('num_relazioni')

    numero_selezioni_docente = {docente.pk: 0 for docente in docenti}

    numero_coautori_possibili_pubblicazione = {}

    for pubblicazione in pubblicazioni:
        numero_coautori_possibili_pubblicazione[pubblicazione.pk] = calcola_numero_coautori_possibili(pubblicazione, relazioni_docente_pubblicazione, docenti)

    for docente in docenti:
        for quartile in [0, 1, 2, 3, 4, 5]:
            for pubblicazione in pubblicazioni.filter(miglior_quartile=quartile):
                if numero_selezioni_docente.get(docente.pk, 0) == numero_selezioni_valutazione:
                    break

                if numero_coautori_possibili_pubblicazione[pubblicazione.pk] == 1 and pubblicazione in pubblicazioni.filter(relazionedocentepubblicazione__autore=docente):
                    relazione = RelazioneDocentePubblicazione.objects.get(pubblicazione=pubblicazione, autore=docente)
                    relazione.scelta = 1
                    relazione.save()
                    numero_selezioni_docente[docente.pk] += 1
                    if numero_selezioni_docente.get(docente.pk, 0) == numero_selezioni_valutazione:
                        break

    return redirect('assegnamento', valutazione)'''


def salva_selezioni(request, valutazione_nome, docente_codice_fiscale):
    valutazione = Valutazione.objects.get(nome=valutazione_nome)
    docente = Docente.objects.get(codiceFiscale=docente_codice_fiscale)

    if request.method == 'POST':
        pubblicazioni = request.POST.getlist('titolo_pubblicazione')
        selezionati = request.POST.getlist('selezione_pubblicazione')

        relazioni_docente_pubblicazione = RelazioneDocentePubblicazione.objects.filter(
            autore=docente)

        set_trace()
        for pubblicazione_id, selezione in zip(pubblicazioni, selezionati):
            relazione = relazioni_docente_pubblicazione.get(
                pubblicazione__titolo=pubblicazione_id)
            if selezione:
                relazione.scelta = 1
            else:
                relazione.scelta = 0
            relazione.save()

    return redirect('assegnamento', valutazione)
