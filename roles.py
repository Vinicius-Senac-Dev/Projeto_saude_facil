# Definindo as permissões de cada perfil.
# Para isso, usamos a biblioteca rolepermissions.

from rolepermissions.roles import AbstractUserRole

class gerente(AbstractUserRole):
    available_permissions = {
        'cadastrar_recepcionista': True,
        'cadastrar_medico': True,
        'cadastrar_farmacias': True,
        'gerenciar_dados': True,
        'gerenciar_especializacoes': True,
        'gerenciar_usuarios': True,
    }

class recepcionista(AbstractUserRole):
    available_permissions = {
        'realizar_cadastro_pacientes': True,
        'Acompanhar_agendamentos': True,
        'Acesso_exames': True,
        'Marcar_consultas': True,
        'Desmarcar_consultas': True,
    }

class medico(AbstractUserRole):
    available_permissions = {
        'prescrever_medicamentos': True,
        'solicitar_exames': True,
        'visualizar_prontuarios': True,
        'atualizar_diagnosticos': True,
    }

class paciente(AbstractUserRole):
    available_permissions = {
        'agendar_consultas': True,
        'visualizar_historico_proprio': True,
        'atualizar_dados_pessoais': True,
        'cancelar_consultas_proprias': True,
    }
