from django.http import HttpResponse


from django.shortcuts import render, redirect

# Create your views here.


from django.contrib.auth import authenticate, login, logout
from django_auth_ldap.backend import LDAPBackend  # Greyed out
from django.contrib.auth.decorators import login_required
from django_auth_ldap.backend import LDAPBackend


def FUR(request):
    return HttpResponse("Hello World!")


def login_view(request):
    if request.method == 'POST':
        # Get info from POST request
        username = request.POST['username']
        pswrd = request.POST['password']
        
        ldap_backend = LDAPBackend()
        user = ldap_backend.authenticate(request, username=username, password=pswrd)
        request.user

        if user is not None:
            user.backend = 'django_auth_ldap.backend.LDAPBackend'
            login(request, user)
            print("Credenziali corrette")
            return redirect('valutazioni')
        else:
            context = {
                'errore': 'Credenziali non corrette, riprovare',
            }
            print("The username and password were incorrect.")
            return render(request, 'login.html', context)
    elif request.method == 'GET':
        return render(request, 'login.html', {})


def logout_view(request):
    logout(request)
    return redirect('valutazioni')