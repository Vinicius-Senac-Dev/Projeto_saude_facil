from django.apps import AppConfig


class UsuariosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'usuarios'
    #Preciso instalar o meu app signals no meu projeto usuarios para funcionar.
    def ready(self):
        import usuarios.signals