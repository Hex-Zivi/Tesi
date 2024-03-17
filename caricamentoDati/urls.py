from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.valutazioni, name="valutazioni"),
    re_path(
        '^inserimento/(?P<anno>\d{4})/(?P<mese>\d{1,2})/$', views.valutazione_per_anno),
        
    path('caricamento/', views.caricamento, name="caricamento"),

    re_path('^caricamento_con_file/(?P<filename>.*)/(?P<valutazione>.*)/$',
            views.caricamento_con_file, name='caricamento_con_file'),

    path('crea_valutazione/', views.crea_valutazione, name='crea_valutazione'),

    path('cancella_valutazione/', views.cancella_valutazione_,
         name='cancella_valutazione'),
    re_path('^cancella_valutazione/(?P<valutazione_nome>.*)/$',
            views.cancella_valutazione, name='cancella_valutazione'),



    path('modifica_valutazione/', views.modifica_valutazione_,
         name='modifica_valutazione'),

    re_path('^modifica_valutazione/(?P<valutazione_nome>.*)/$',
            views.modifica_valutazione, name="modifica_valutazione"),

    path('cancella_pubblicazioni_tot/', views.cancella_pubblicazioni_tot_,
         name='cancella_pubblicazioni_tot'),

    re_path('^cancella_pubblicazioni_tot/(?P<valutazione_nome>.*)/$', views.cancella_pubblicazioni_tot,
         name='cancella_pubblicazioni_tot'),

     re_path('^cancella_pubblicazione_singola/(?P<valutazione_nome>.*)/(?P<pubblicazione_titolo>.*)/$', views.cancella_pubblicazione_singola,
         name='cancella_pubblicazione_singola'),

     re_path('^assegnamento/(?P<valutazione_nome>.*)/$',
            views.assegnamento, name="assegnamento"),

     re_path('^docente_pubblicazioni/(?P<valutazione_nome>.*)/(?P<docente_codice_fiscale>.*)/$',
            views.docente_pubblicazioni, name="docente_pubblicazioni"),
]
