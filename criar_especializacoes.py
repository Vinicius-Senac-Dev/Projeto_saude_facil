import os
import django
import sys

# Configurar o Django
sys.path.append(r'c:\Users\caue53775816\OneDrive - SENAC DF\Área de Trabalho\PI\Projeto_saude_facil')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'saude_facil.settings')
django.setup()

from usuarios.models import Especializacao

especializacoes = [
    'Cardiologia',
    'Dermatologia', 
    'Pediatria',
    'Clínica Geral',
    'Ortopedia',
    'Ginecologia',
    'Neurologia',
    'Psiquiatria'
]

for nome in especializacoes:
    esp, created = Especializacao.objects.get_or_create(nome=nome)
    if created:
        print(f"Especialização '{nome}' criada!")
    else:
        print(f"Especialização '{nome}' já existe")

print("\n✅ Especializações criadas com sucesso!")
