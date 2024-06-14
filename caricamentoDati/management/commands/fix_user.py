
from django.core.management.base import BaseCommand
from django.contrib.admin.models import LogEntry
from django.db import transaction, connection
from caricamentoDati.models import CustomUser

class Command(BaseCommand):
    help = 'Aggiungi o aggiorna gli utenti mancanti nella tabella auth_user per risolvere i problemi di chiave esterna in django_admin_log'

    def handle(self, *args, **kwargs):
        # Trova user_id mancanti
        log_entries = LogEntry.objects.values_list('user_id', flat=True).distinct()
        # Esegui query SQL grezze per ottenere gli ID esistenti in auth_user
        utenti=CustomUser.objects.all()
        with connection.cursor() as cursor:
            cursor.execute("SELECT id FROM auth_user")
            existing_users = [row[0] for row in cursor.fetchall()]

        missing_user_ids = set(log_entries) - set(existing_users)

        # Aggiungi o aggiorna utenti mancanti in una transazione atomica
        with transaction.atomic():
            for utente in utenti:
                try:
                    user_id = utente.id
                    username = utente.username
                    password = utente.password
                    first_name = utente.first_name
                    last_name = utente.last_name
                    email = utente.email if utente.email else "mail@mail.com"
                    is_superuser = utente.is_superuser
                    is_staff = utente.is_staff
                    date_joined = utente.date_joined
                    is_active = utente.is_active

                    if user_id in existing_users:
                        # Aggiorna utente esistente
                        with connection.cursor() as cursor:
                            cursor.execute("""
                                UPDATE auth_user
                                SET username = %s, password = %s, first_name = %s, last_name = %s, email = %s, is_superuser = %s, is_staff = %s, date_joined = %s, is_active = %s
                                WHERE id = %s
                            """, [username, password, first_name, last_name, email, is_superuser, is_staff, date_joined, is_active, user_id])
                        self.stdout.write(self.style.SUCCESS(
                            f'Utente aggiornato con successo: {username} (id: {user_id})'))
                    else:
                        # Crea nuovo utente
                        with connection.cursor() as cursor:
                            cursor.execute("""
                                INSERT INTO auth_user (id, username, password, first_name, last_name, email, is_superuser, is_staff, date_joined, is_active)
                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                            """, [user_id, username, password, first_name, last_name, email, is_superuser, is_staff, date_joined, is_active])
                        self.stdout.write(self.style.SUCCESS(
                            f'Utente creato con successo: {username} (id: {user_id})'))
                except CustomUser.DoesNotExist:
                    self.stdout.write(self.style.ERROR(
                        f'Utente con id {user_id} non trovato nel modello CustomUser'))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(
                        f'Errore durante la creazione o l\'aggiornamento dell\'utente {user_id}: {str(e)}'))
                    raise

        self.stdout.write(self.style.SUCCESS(
            f'Aggiunti o aggiornati {len(missing_user_ids)} utenti mancanti.'))

        # Stampa i dati della tabella auth_user ordinati per id
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM auth_user ORDER BY id ASC")
            users = cursor.fetchall()
        
        self.stdout.write(self.style.SUCCESS('Dati nella tabella auth_user:'))
        for user in users:
            self.stdout.write(str(user))
