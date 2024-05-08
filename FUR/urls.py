"""FUR URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path

from FUR import views
from caricamentoDati import views as views_caricamentoDati

urlpatterns = [
    path('admin/', admin.site.urls),
    path('FUR/', views.FUR, name='FUR'),
    path('valutazioni/', include('caricamentoDati.urls')),
    path('accounts/login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    #path('caricamento/', include('caricamentoDati.urls')),
    #path('caricamento_con_file/', include('caricamentoDati.urls')),
    #path('caricamento/', views_caricamentoDati.caricamento, name='caricamento'),
    #path('^caricamento_con_file/(?P<csv_file_name>\(.*))/$', views_caricamentoDati.caricamento_con_file, name='caricamento_con_file'),
]
