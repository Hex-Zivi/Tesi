from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.valutazioni, name="valutazioni"),
    re_path(
        '^inserimento/(?P<anno>\d{4})/(?P<mese>\d{1,2})/$', views.valutazione_per_anno),
]
