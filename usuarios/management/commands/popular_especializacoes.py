from django.core.management.base import BaseCommand
from usuarios.models import Especializacao


class Command(BaseCommand):
    help = 'Popula o banco de dados com especializações médicas básicas'

    def handle(self, *args, **options):
        especializacoes = [
            {
                'nome': 'Cardiologia',
                'descricao': 'Especialidade médica que se ocupa do diagnóstico e tratamento das doenças que acometem o coração bem como os outros componentes do sistema circulatório.',
                'codigo_cbo': '2251-06'
            },
            {
                'nome': 'Dermatologia',
                'descricao': 'Especialidade médica que se ocupa do diagnóstico, prevenção e tratamento de doenças e afecções relacionadas à pele, pelos, mucosas, cabelo e unhas.',
                'codigo_cbo': '2251-08'
            },
            {
                'nome': 'Endocrinologia',
                'descricao': 'Especialidade médica que cuida dos transtornos das glândulas endócrinas, como diabetes, tireóide, obesidade, etc.',
                'codigo_cbo': '2251-10'
            },
            {
                'nome': 'Ginecologia',
                'descricao': 'Especialidade médica que trata de doenças do sistema reprodutor feminino, útero, vagina e ovários.',
                'codigo_cbo': '2251-12'
            },
            {
                'nome': 'Neurologia',
                'descricao': 'Especialidade médica que trata dos distúrbios estruturais do sistema nervoso.',
                'codigo_cbo': '2251-42'
            },
            {
                'nome': 'Oftalmologia',
                'descricao': 'Especialidade médica que investiga e trata as doenças relacionadas aos olhos, à refração e aos olhos e seus anexos.',
                'codigo_cbo': '2251-46'
            },
            {
                'nome': 'Ortopedia',
                'descricao': 'Especialidade médica que cuida das doenças e deformidades dos ossos, músculos, ligamentos, articulações.',
                'codigo_cbo': '2251-48'
            },
            {
                'nome': 'Pediatria',
                'descricao': 'Especialidade médica dedicada à assistência à criança e ao adolescente, nos seus diversos aspectos.',
                'codigo_cbo': '2251-50'
            },
            {
                'nome': 'Psiquiatria',
                'descricao': 'Especialidade médica que trata da prevenção, atendimento, diagnóstico, tratamento e reabilitação das diferentes formas de sofrimentos mentais.',
                'codigo_cbo': '2251-52'
            },
            {
                'nome': 'Urologia',
                'descricao': 'Especialidade médica que trata do trato urinário de homens e de mulheres e do sistema reprodutor das pessoas do sexo masculino.',
                'codigo_cbo': '2251-78'
            },
            {
                'nome': 'Clínica Geral',
                'descricao': 'Especialidade médica que trata de pacientes adultos, atuando principalmente em ambiente ambulatorial.',
                'codigo_cbo': '2251-02'
            },
            {
                'nome': 'Medicina da Família',
                'descricao': 'Especialidade médica que presta cuidados de saúde abrangentes e contínuos ao indivíduo e à família.',
                'codigo_cbo': '2251-32'
            }
        ]

        for esp_data in especializacoes:
            especializacao, created = Especializacao.objects.get_or_create(
                nome=esp_data['nome'],
                defaults={
                    'descricao': esp_data['descricao'],
                    'codigo_cbo': esp_data['codigo_cbo']
                }
            )
            
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Especialização "{especializacao.nome}" criada com sucesso')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Especialização "{especializacao.nome}" já existe')
                )

        self.stdout.write(
            self.style.SUCCESS('\nTodas as especializações foram processadas!')
        )
