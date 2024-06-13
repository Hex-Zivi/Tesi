from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.admin.models import LogEntry
from django.db import transaction

class Command(BaseCommand):
    help = 'Aggiungi gli utenti mancanti nella tabella auth_user'

    def handle(self, *args, **kwargs):
        User = get_user_model()
        missing_users = []

        # Trova user_id mancanti
        log_entries = LogEntry.objects.values_list('user_id', flat=True).distinct()
        existing_users = User.objects.values_list('id', flat=True)
        missing_user_ids = set(log_entries) - set(existing_users)

        if not missing_user_ids:
            self.stdout.write(self.style.SUCCESS('Nessun utente mancante trovato.'))
            return

        # Aggiungi utenti mancanti
        with transaction.atomic():
            for user_id in missing_user_ids:
                try:
                    User.objects.create(id=user_id, username=f'user_{user_id}')
                    missing_users.append(user_id)
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Errore durante la creazione dell\'utente {user_id}: {str(e)}'))

        self.stdout.write(self.style.SUCCESS(f'Aggiunti {len(missing_users)} utenti mancanti.'))
        if missing_users:
            self.stdout.write(self.style.WARNING(f'Utenti aggiunti: {missing_users}'))
