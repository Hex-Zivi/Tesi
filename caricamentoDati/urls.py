from django.urls import path, re_path
from . import views

urlpatterns = [

    path('login', views.login, name="login"),

    path('', views.valutazioni, name="valutazioni"),

    re_path(
        '^inserimento/(?P<anno>\d{4})/(?P<mese>\d{1,2})/$', views.valutazione_per_anno),

    path('caricamento/', views.caricamento, name="caricamento"),

    re_path('^caricamento_con_file/(?P<filename>.*)/(?P<valutazione>.*)/$',
            views.caricamento_con_file, name='caricamento_con_file'),

    path('crea_valutazione/', views.crea_valutazione, name='crea_valutazione'),


    re_path('^cancella_valutazione/(?P<valutazione_nome>.*)/$',
            views.cancella_valutazione, name='cancella_valutazione'),

    re_path('^modifica_valutazione/(?P<valutazione_nome>.*)/$',
            views.modifica_valutazione, name="modifica_valutazione"),

    re_path('^aggiungi_pubblicazione_pagina/(?P<valutazione_nome>.*)/(?P<caller>.*)/(?P<docente>.*)/$',
            views.aggiungi_pubblicazione_pagina, name="aggiungi_pubblicazione_pagina"),

    re_path('^aggiungi_pubblicazione/(?P<valutazione_nome>.*)/(?P<docente>.*)/$',
            views.aggiungi_pubblicazione, name="aggiungi_pubblicazione"),

    re_path('^cancella_pubblicazioni_tot/(?P<valutazione_nome>.*)/$', views.cancella_pubblicazioni_tot,
            name='cancella_pubblicazioni_tot'),

    re_path('^cancella_pubblicazione_singola/(?P<valutazione_nome>.*)/(?P<pubblicazione_titolo>.*)/$', views.cancella_pubblicazione_singola,
            name='cancella_pubblicazione_singola'),

    re_path('^assegnamento/(?P<valutazione_nome>.*)/$',
            views.assegnamento, name="assegnamento"),

    re_path('^assegnamento_algoritmo/(?P<valutazione_nome>.*)/$',
            views.assegnamento_algoritmo, name="assegnamento_algoritmo"),

    re_path('^azzera_assegnamento/(?P<valutazione_nome>.*)/$',
            views.azzera_assegnamento, name="azzera_assegnamento"),

    re_path('^docente_pubblicazioni/(?P<valutazione_nome>.*)/(?P<docente_codice_fiscale>.*)/$',
            views.docente_pubblicazioni, name="docente_pubblicazioni"),

    re_path('^salva_selezioni/(?P<valutazione_nome>.*)/(?P<docente_codice_fiscale>.*)/$',
            views.salva_selezioni, name="salva_selezioni"),

    re_path('^riviste_eccellenti/(?P<valutazione_nome>.*)/$',
            views.riviste_eccellenti, name="riviste_eccellenti"),

    re_path('^carica_riviste/(?P<valutazione_nome>.*)/$',
            views.carica_riviste, name="carica_riviste"),

]
