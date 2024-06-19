from django.urls import path, re_path
from . import views

urlpatterns = [

    # VALUTAZIONI

    # Vista principale
    path('', views.valutazioni, name="valutazioni"),

    # Crea una nuova valutazione
    path('crea_valutazione/', views.crea_valutazione,
         name='crea_valutazione'),

    # Cancella una valutazione
    re_path('^cancella_valutazione/(?P<valutazione_nome>.*)/$',
            views.cancella_valutazione, name='cancella_valutazione'),

    # Chiude una valutazione
    re_path('^chiudi valutazione/(?P<valutazione_nome>.*)/$', views.chiudi_valutazione,
            name='chiudi_valutazione'),

    # Esporta il file contenente le pubblicazioni selezionate per la valutazione
    re_path('^esporta/(?P<valutazione_nome>.*)/$',
            views.esporta_csv, name='esporta_csv'),



    # MODIFICA

    # Apre la pagina pe la modifica di una valutazione
    re_path('^modifica_valutazione/(?P<valutazione_nome>.*)/$',
            views.modifica_valutazione, name="modifica_valutazione"),

    # Caricamento delle pubblicazioni con file csv
    re_path('^caricamento_con_file/(?P<filename>.*)/(?P<valutazione>.*)/$',
            views.caricamento_con_file, name='caricamento_con_file'),

    # Cancella tutte le pubblicazioni per una valutazione
    re_path('^cancella_pubblicazioni_tot/(?P<valutazione_nome>.*)/$', views.cancella_pubblicazioni_tot,
            name='cancella_pubblicazioni_tot'),

    # Cancella una singola pubblicazione
    re_path('^cancella_pubblicazione_singola/(?P<valutazione_nome>.*)/(?P<pubblicazione_slug>.*)/$',
            views.cancella_pubblicazione_singola, name='cancella_pubblicazione_singola'),



    # AGGIUNGI PUBBLICAZIONE

    # Apre la pagina per l'aggiunta di pubblicazioni
    re_path('^aggiungi_pubblicazione_pagina/(?P<valutazione_nome>.*)/(?P<caller>.*)/(?P<docente>.*)/$',
            views.aggiungi_pubblicazione_pagina, name="aggiungi_pubblicazione_pagina"),

    # Aggiunge una pubblicazione specificata
    re_path('^aggiungi_pubblicazione/(?P<valutazione_nome>.*)/(?P<docente>.*)/(?P<caller>.*)/$',
            views.aggiungi_pubblicazione, name="aggiungi_pubblicazione"),



    # RIVISTE ECCELLENTI

    # Mostra la pagina di gestione delle riviste eccellenti per una valutazione
    re_path('^riviste_eccellenti/(?P<valutazione_nome>.*)/$',
            views.riviste_eccellenti, name="riviste_eccellenti"),

    # Carica le riviste ecccellenti per una valutazione
    re_path('^carica_riviste/(?P<valutazione_nome>.*)/$',
            views.carica_riviste, name="carica_riviste"),

    # Cancella le riviste per una valutazione
    re_path('^cancella_riviste/(?P<valutazione_nome>.*)/$', views.cancella_riviste,
            name='cancella_riviste'),



    # ASSEGNAMENTO

    # Apre la pagina per l'assegnamento per una valutazione
    re_path('^assegnamento/(?P<valutazione_nome>.*)/$',
            views.assegnamento, name="assegnamento"),

    # Esegue l'assegnamento automatico per una valutazione
    re_path('^assegnamento_algoritmo/(?P<valutazione_nome>.*)/$',
            views.assegnamento_algoritmo, name="assegnamento_algoritmo"),

    # Azzera l'assegnamento per una valutazione
    re_path('^azzera_assegnamento/(?P<valutazione_nome>.*)/$',
            views.azzera_assegnamento, name="azzera_assegnamento"),



    # DOCENTE-PUBBLICAZIONI

    # Mostra la pagina di selezione delle pubblicazioni di un docente per una valutazione
    re_path('^docente_pubblicazioni/(?P<valutazione_nome>.*)/(?P<docente_codice_fiscale>.*)/$',
            views.docente_pubblicazioni, name="docente_pubblicazioni"),

    # Salva le selezioni effettuate per un docente
    re_path('^salva_selezioni/(?P<valutazione_nome>.*)/(?P<docente_codice_fiscale>.*)/$',
            views.salva_selezioni, name="salva_selezioni"),



    # SELEZIONI

    # Apre la pagine che mostra le selezioni per una valutazione
    re_path('^selezioni/(?P<valutazione_nome>.*)/$', views.visualizza_selezioni,
            name='selezioni'),
]
