from django.core.management.base import BaseCommand
from django.core.management import call_command

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('arambikalamey 😎'))
        call_command('runserver', '127.0.0.1:8000')
        
         