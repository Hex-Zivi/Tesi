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
]
