#Definindo as permissões de cada perfil.
#Para isso, usamos a biblioteca rolepermissions.

from rolepermissions.roles import AbstractUserRole

class Gerente(AbstractUserRole):
    available_permissions = {
        'Cadastrar_recepcionista': True,
        'Cadastrar_medico': True,
        'Cadastrar_farmacias': True,
    }

    class Recepcionista(AbstractUserRole):
        available_permissions = {
            'realizar_cadastro_pacientes': True,
            'Acompanhar_agendamentos': True,
            'Acesso_exames': True,
            'Marcar_consultas': True,
            'Desmarcar_consultas': True,
        }