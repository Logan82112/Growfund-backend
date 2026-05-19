"""
Management command to run migrations via web endpoint
"""
from django.core.management.base import BaseCommand
from django.core.management import call_command
from io import StringIO


class Command(BaseCommand):
    help = 'Run migrations and setup commands'

    def handle(self, *args, **options):
        output = StringIO()
        
        self.stdout.write(self.style.SUCCESS('🔄 Running database migrations...'))
        call_command('migrate', '--noinput', stdout=output, stderr=output)
        self.stdout.write(output.getvalue())
        
        self.stdout.write(self.style.SUCCESS('⚙️ Setting up platform settings...'))
        try:
            call_command('setup_platform_settings', stdout=output, stderr=output)
            self.stdout.write(output.getvalue())
        except Exception as e:
            self.stdout.write(self.style.WARNING(f'Platform settings: {e}'))
        
        self.stdout.write(self.style.SUCCESS('💰 Setting up crypto prices...'))
        try:
            call_command('setup_crypto_prices', stdout=output, stderr=output)
            self.stdout.write(output.getvalue())
        except Exception as e:
            self.stdout.write(self.style.WARNING(f'Crypto prices: {e}'))
        
        self.stdout.write(self.style.SUCCESS('✅ All setup complete!'))
