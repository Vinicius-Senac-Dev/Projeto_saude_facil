from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from usuarios.models import Especializacao, DadosMedico
from tela_principal.models import HorarioAtendimento
from rolepermissions.roles import assign_role
import datetime

User = get_user_model()


class Command(BaseCommand):
    help = 'Cria dados de teste para o sistema de agendamento'

    def handle(self, *args, **options):
        # Criar usuário gerente
        gerente, created = User.objects.get_or_create(
            username='gerente',
            defaults={
                'email': 'gerente@saudefacil.com',
                'first_name': 'João',
                'last_name': 'Silva',
                'cargo': 'G',
                'is_staff': True,
            }
        )
        if created:
            gerente.set_password('123456')
            gerente.save()
            assign_role(gerente, 'gerente')
            self.stdout.write(self.style.SUCCESS(f'Gerente criado: {gerente.username}'))
        
        # Criar médicos de teste
        medicos_data = [
            {
                'username': 'dr_carlos',
                'email': 'carlos@saudefacil.com',
                'first_name': 'Carlos',
                'last_name': 'Santos',
                'crm': '12345',
                'uf_crm': 'DF',
                'especializacoes': ['Cardiologia', 'Clínica Geral'],
                'valor_consulta': 150.00,
            },
            {
                'username': 'dra_maria',
                'email': 'maria@saudefacil.com',
                'first_name': 'Maria',
                'last_name': 'Oliveira',
                'crm': '67890',
                'uf_crm': 'DF',
                'especializacoes': ['Dermatologia', 'Clínica Geral'],
                'valor_consulta': 180.00,
            },
            {
                'username': 'dr_pedro',
                'email': 'pedro@saudefacil.com',
                'first_name': 'Pedro',
                'last_name': 'Costa',
                'crm': '11111',
                'uf_crm': 'DF',
                'especializacoes': ['Pediatria'],
                'valor_consulta': 120.00,
            },
        ]
        
        for medico_data in medicos_data:
            # Criar usuário médico
            medico, created = User.objects.get_or_create(
                username=medico_data['username'],
                defaults={
                    'email': medico_data['email'],
                    'first_name': medico_data['first_name'],
                    'last_name': medico_data['last_name'],
                    'cargo': 'M',
                }
            )
            if created:
                medico.set_password('123456')
                medico.save()
                assign_role(medico, 'medico')
                self.stdout.write(self.style.SUCCESS(f'Médico criado: {medico.username}'))
            
            # Criar dados médicos
            dados_medico, created = DadosMedico.objects.get_or_create(
                usuario=medico,
                defaults={
                    'crm': medico_data['crm'],
                    'uf_crm': medico_data['uf_crm'],
                    'valor_consulta': medico_data['valor_consulta'],
                    'tempo_consulta': 30,
                    'horario_inicio': datetime.time(8, 0),
                    'horario_fim': datetime.time(17, 0),
                    'dias_semana': '1,2,3,4,5',  # Segunda a sexta
                    'biografia': 'Médico especialista com ampla experiência.',
                }
            )
            
            if created:
                # Adicionar especializações
                for esp_nome in medico_data['especializacoes']:
                    try:
                        especialidade = Especializacao.objects.get(nome=esp_nome)
                        dados_medico.especializacoes.add(especialidade)
                    except Especializacao.DoesNotExist:
                        self.stdout.write(
                            self.style.WARNING(f'Especialização "{esp_nome}" não encontrada')
                        )
                
                self.stdout.write(
                    self.style.SUCCESS(f'Dados médicos criados para {medico.get_full_name()}')
                )
            
            # Criar horários de atendimento
            for dia in range(1, 6):  # Segunda a sexta
                HorarioAtendimento.objects.get_or_create(
                    medico=medico,
                    dia_semana=dia,
                    hora_inicio=datetime.time(8, 0),
                    hora_fim=datetime.time(17, 0),
                )
        
        # Criar paciente de teste
        paciente, created = User.objects.get_or_create(
            username='paciente_teste',
            defaults={
                'email': 'paciente@teste.com',
                'first_name': 'Ana',
                'last_name': 'Silva',
                'cargo': 'P',
                'cpf': '12345678901',
                'telefone': '(61) 99999-9999',
            }
        )
        if created:
            paciente.set_password('123456')
            paciente.save()
            assign_role(paciente, 'paciente')
            self.stdout.write(self.style.SUCCESS(f'Paciente criado: {paciente.username}'))
        
        self.stdout.write(
            self.style.SUCCESS('\n✅ Dados de teste criados com sucesso!')
        )
        self.stdout.write(
            self.style.SUCCESS('\nCredenciais de acesso:')
        )
        self.stdout.write('• Gerente: gerente / 123456')
        self.stdout.write('• Médicos: dr_carlos, dra_maria, dr_pedro / 123456')
        self.stdout.write('• Paciente: paciente_teste / 123456')
