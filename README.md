# furapp

Lo scopo di questo programma è semplificare la gestione e l'estrazione delle pubblicazioni dei docenti universitari per il calcolo del fondo FUR. L'obiettivo è creare un portale che permetta l'estrazione automatica delle pubblicazioni e la selezione manuale da parte degli autori, rendendo il processo semplice e intuitivo.

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

### Lato applicazione

Ogni utente aprendo la pagina verrà immediatamente indirizzato alla pagina di login e potrà accedere utilizzando le proprie credernziali GIA.

Per entrambi gli utilizzi, abmministrazione e utente, è impostato un timer di sessione della durata di un'ora, modificabile in FUR/settings.py:

```python
# Session timeout
SESSION_EXPIRE_SECONDS = 3600  # secondi

SESSION_EXPIRE_AFTER_LAST_ACTIVITY = True

SESSION_TIMEOUT_REDIRECT = '/'
```

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

## L'algoritmo

L'algoritmo di estrazione segue un ordine di precedenza:

Questa porzione viene eseguita solo una volta

1. Selezione delle pubblicazioni appartenenti alle riviste eccellenti (per peso maggiore)

2. Selezione delle pubblicazioni per autori con numero di pubblicazioni inferiore o uguale al numero richiesto (per massimizzare il numero di selezioni)

Questa porzione viene ripetuta ciclicamente in modo che l'agoritmo cerchi di assegnare le pubblicazioni con peso maggiore

3. Selezione delle pubblicazioni con quartile uguale a 0 o 1 e con singolo autore (per peso maggiore e migliore selezione)

Da qui in poi l'algoritmo cerca di assegnare le pubblicazioni massimizzandone il valore, ma con la difficoltà di dover "risolvere" i conflitti

4. Selezione di pubblicazioni con autori multipli con quartile uguale a 0 o 1, sulla base degli autori che hanno già raggiunto il numero massimo di pubblicazioni da assegnare

5. Come il punto 3, ma con qurtile uguale a 2

6. Come il punto 4, ma con quartile uguale a 2

7. Come i punti 3 e 5, ma con quartili uguali o maggiori di 3

8. Come i punti 4 e 6, ma con quartili uguali o maggiori di 3

Resta la possibilità che alla fine dell'esecuzione dell'algoritmo, alcuni autori non abbiano raggiunto il numero di pubblicazioni richieste. Nella pagina di assegnamento (a disposizione per l'amministrazione), e possibile vedere quali sono i casi per i quali è necessario intervenire manualomente (per troppi conflitti), oppure semplicemente non sono disponibili abbastanza pubblicazioni.


## NOTA

Il file CSV per l'importazione delle pubblicazioni segue un formato ben specifico.
Questo formato può essere rispettato nei file csv, oppure, per comodità, è possibile modificare la vista per il caricamento e adattarlo al formato più conveniente in caricamentoDati/views.py, modificando:

```python
def caricamento_con_file(request, filename, valutazione):
    if request.method == 'POST':
        file = request.FILES.get('filename')
        valutazione = Valutazione.objects.get(nome=valutazione)
        elenco = []
        intestazione = ['anno_di_pubblicazione', 'autore', 'codice_fiscale', 'handle', 'doi', 'titolo',
                        'tipologia_collezione',
                        'issn_o_isbn', 'titolo_rivista_o_atti', 'indicizzato_scopus', 'miglior_quartile_scopus',
                        'num_coautori_interni_dip', 'codice_fiscale']
        riferimento = []
        if file:
            # Determina il tipo di file
            if file.name.endswith('.csv'):
                csv_data = csv.reader(file.read().decode(
                    'utf-8').splitlines(), delimiter=',')
                for valore in csv_data:
                    elenco.append(valore)
            elif filename.endswith('.xlsx'):
                workbook = openpyxl.load_workbook(file)
                sheet = workbook.active
                for row in sheet.iter_rows(values_only=True):
                    elenco.append(row)
            else:
                # Gestisci il caso in cui il tipo di file non è supportato
                return HttpResponse("Il tipo di file non è supportato.")

            for element in elenco[5]:
                for titolo in intestazione:
                    if element.lower() == titolo:
                        riferimento.append(intestazione.index(titolo))

            with transaction.atomic():

                # In assenza di un file di caricamento veritiero, ho aggiunto una colonna per il codice fiscale alla fine: modificare i numeri delle colonne in maniera consona
                for riga in elenco[6:]:
                    anno_pubblicazione = riga[0]
                    autore = riga[1]
                    handle = riga[2]
                    doi = riga[3]
                    titolo = riga[4]
                    tipologia_collezione = riga[5]
                    issn_isbn = riga[6]
                    titolo_rivista_atti = riga[7]
                    titolo_rivista_atti = titolo_rivista_atti.upper()
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

        if valutazione.status == "Vuota":
            valutazione.status = "Pubblicazioni caricate"
            valutazione.dataCaricamentoPubblicazioni = datetime.date.today()
            valutazione.save()

    return redirect('modifica_valutazione', valutazione)
```

## Shema sql

Per ottenere uno schema SQL del database è possibile esportarlo col comado da terminale:

```bash
pg_dump -U myuser -s -f schema.sql mydatabase
```

## Ringraziamenti

Desidero esprimere la mia sincera gratitudine ai seguenti individui per il loro supporto e i loro preziosi consigli durante lo sviluppo di questo progetto:

- Dr. Belussi Alberto, per la sua guida.
- Dott.ssa Migliorini Sara, per il suo supporto costante.
- Dott.ssa Dalla Vecchia Anna, per il suo contributo per l'implementazione dell'algoritmo di selezione.
- Zanetti Alex, per le impostazioni del server LDAP e i modelli interni di base.