from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.conf import settings

class Command(BaseCommand):
    help = 'Testa o envio de emails'

    def add_arguments(self, parser):
        parser.add_argument('--to', type=str, help='Email de destino', required=True)

    def handle(self, *args, **options):
        email_destino = options['to']
        
        try:
            send_mail(
                subject='Teste de Email - Saúde Fácil',
                message='''Este é um email de teste do sistema Saúde Fácil.

Se você recebeu este email, significa que a configuração está funcionando corretamente!

Configuração atual:
- Backend: {backend}
- Host: {host}
- Porta: {port}

Teste realizado com sucesso!

Equipe Saúde Fácil'''.format(
                    backend=settings.EMAIL_BACKEND,
                    host=getattr(settings, 'EMAIL_HOST', 'Console'),
                    port=getattr(settings, 'EMAIL_PORT', 'N/A')
                ),
                from_email=None,
                recipient_list=[email_destino],
                fail_silently=False,
            )
            self.stdout.write(
                self.style.SUCCESS(f'Email de teste enviado com sucesso para {email_destino}')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Erro ao enviar email: {e}')
            )
