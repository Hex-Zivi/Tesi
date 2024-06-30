# furapp

## Preparazione Iniziale
### Installazione

Per installare il progetto, segui questi passaggi:

1. Clona il repository:
   ```bash
   git clone https://github.com/tuo-username/tuo-progetto-django.git
   cd tuo-progetto-django

   ```

2. Entrare nella cartella e aprire un terminale.
   Eseguire il comando per l'installazione dei pacchetti:
   
   ```bash
   pip install -r requirements.txt
   ```
### Configurazione dell'url

Configurare l'url in FUR/settings.py:

```python
ALLOWED_HOSTS = ['localhost']
ALLOWED_HOSTS=['127.0.0.1']
#ALLOWED_HOSTS = []
```


Ed disattivare il debugger impostando in FUR/settings.py:
```python
DEBUG = False
```

### Configurazione del Database

FUR/settings.py, modifica la configurazione del database a seconda delle tue necessità. Attualmente, è impostato su PostgreSQL. Per ulteriori informazioni, consulta la [pagina di Django](https://docs.djangoproject.com/en/5.0/ref/databases/):

```python
DATABASES = {
        'default': {
                'ENGINE': 'django.db.backends.postgresql_psycopg2',
                'NAME': 'nome_base_di_dati',
                'USER': 'utente',
                'PASSWORD': '######',
                'HOST': 'localhost',
                'PORT': '5432',
        }
}
```

### Configurazione del server LDAP

FUR/settings.py modifica la configurazione del server LDAP a seconda delle tue necessità:

```python
AUTH_LDAP_SERVER_URI = 'ldap://localhost'
LDAP_DOMAIN = "dc=univr,dc=it"

AUTH_LDAP_BIND_DN = f'cn=admin,{LDAP_DOMAIN}'
AUTH_LDAP_BIND_PASSWORD = 'test1234'
AUTH_LDAP_USER_SEARCH = LDAPSearch(
    f'{LDAP_DOMAIN}',
    ldap.SCOPE_SUBTREE,
    '(uid=%(user)s)',
)


AUTH_LDAP_USER_ATTR_MAP = {
    'first_name': 'givenName',
    'last_name': 'sn',
    'codice_fiscale': 'univrCF',
    'ruolo': 'objectclass',
    'uid': 'uidnumber'
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
    ),
}

AUTHENTICATION_BACKENDS = (
    "django_auth_ldap.backend.LDAPBackend",
    "django.contrib.auth.backends.ModelBackend",
)
```

### Migrazione del Database

Per collegare la base di dati è sufficiente usare i comandi:

```bash
python3 manage.py makemigrations
python3 manage.py migrate
```

In questo modo si creeranno i modelli necessari al funzionamento. Successivamente, bisogna configurare il modello utente personalizzato (CustomUser) come utente di default di Django.

In FUR/settings.py, aggiungi:

```python
AUTH_USER_MODEL = 'caricamentoDati.CustomUser'
```

Esegui nuovamente le migrazioni:

```bash
python3 manage.py makemigrations
python3 manage.py migrate
```

## Primo utilizzo

Prima di poter utilizzare il programma è necessario creare un superutente che possa accedere alla pagina di amministrazione

### Creare un superuser
Aprire un terminale nella cartella principale e usare il comando:

```python
python3 manage.py createsuperuser
```

E seguire la procedura, sarà necessario fornire un Username, una mail e una password

A questo punto sarà possibile avviare il server

```bash
python3 manage.py runserver
```

Gli Utenti potranno accedere al server con le proprie credenziali GIA.

Il superutente può accedere alla pagina di amministrazione:

```url
[url_dell'applicazione]/admin
```

Ed impostare manualmente i permessi.

In alternativa si possono impostare metodi di riconoscimento autmatico, avendo la struttura del server LDAP al login modificando FUR/views.py

</br>
</br>


## Utilizzo

### Lato server

Prima che il programma possa essere utilizzato dagli utenti è necessario avviare il server.
Aprire un terminale nella cartella contenente il programma (contiene il file manage.py) e utilizzare il comando:

```bash
python3 manage.py runserver
```

### Lato utente

Ogni utente aprendo la pagina verrà immediatamente indirizzato alla pagina di login e potrà accedere utilizzando le proprie credernziali GIA

#### Amministrazione

Nella schermata iniziale l'amministrazione avrà a disposizione l'elenco delle Valutazioni già caricate, ordinate in ordine decrescente di data, e un modulo per aggiungere nuove Valutazioni (richiede tre campi: Nome, Anno e Numero di pubblicazioni da assegnare)

Per ogni valutazione viene mostrato il suo stato e una serie di pulsanti che rimandano a diverse pagine

1. Modifica, permette di:
   1. Permette di caricare le pubblicazioni da un file CSV
   2. Aggiungere singole pubblicazioni
   3. Gestire le Riviste Eccellenti


2. Assegna Pubblicazioni, permette di:
   1. Utilizzare l'algoritmo di selezione
   2. Azzerare tutte le selezioni effettuate
   3. Aggiungere singole pubblicazioni
   4. Visualizzare le selezioni
   5. Accedere alle singole pubblicazione per autore per la selezione manuale


3. Cancella, per eliminare la Valutazione
4. Chiudi, per chiudere la valutazione e permettere l'esportazione
5. Visualizza Selezioni
6. Esporta CSV per: Esportare le selezioni (solo se la valutazione è chiusa)


#### Utente

L'utente ha solo la possibilità di accedere alle proprie pubblicazioni contenute nelle Valutazioni per la selezione ed eventualmente aggiungerne.