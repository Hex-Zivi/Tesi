from django.http import HttpResponse

import csv
import datetime
from django.db import transaction

from django.shortcuts import render, redirect

# Create your views here.


from django.db.models import Count

from django.http import JsonResponse

import requests
from bs4 import BeautifulSoup
import openpyxl

from django.contrib.auth import authenticate, login, logout
from django_auth_ldap.backend import LDAPBackend  # Greyed out
from django.contrib.auth.decorators import login_required
from django_auth_ldap.backend import LDAPBackend


def FUR(request):
    return HttpResponse("Hello World!")


def login_view(request):
    if request.method == 'POST':
        # Get info from POST request
        usr = request.POST['username']
        pas = request.POST['password']

        ldap_backend = LDAPBackend()
        user = ldap_backend.authenticate(request, username=usr, password=pas)
        request.user
        print(user)

        # Da controllare
        user_attrs = user.ldap_user._user_attrs._data['objectclass']
        user.ruolo = 'admin' if 'univrUtente' in user_attrs else 'user'
        # // Da controllare


        if user is not None:
            user.backend = 'django_auth_ldap.backend.LDAPBackend'
            login(request, user)
            print(user.codice_fiscale, user.ruolo, user.first_name, user.last_name, user.uid)
            print("Credenziali corrette")
            return redirect('valutazioni')
        else:
            print("The username and password were incorrect.")
            return render(request, 'dashboard/error.html', {})
    elif request.method == 'GET':
        return render(request, 'login.html', {})


def logout_view(request):
    logout(request)  # Esegui il logout dell'utente
    return redirect('valutazioni')  # Reindirizza alla pagina di login
