from django.dispatch import receiver
#O receiver observa se houve uma mudança de estado na classe
from django.db.models.signals import post_save
#post_save quando o metodo save, que é o metodo que salva no banco, for executado chamamos o signals, depois de salvar no banco, vai ocorrer a ação.
from .models import Users
from rolepermissions.roles import assign_role
#assign_role vai definir qual é a permissão que ele tem.

@receiver(post_save, sender=Users)

def define_permissoes(sender, instance, created, **kwargs):
    if created:
        if instance.cargo == "R":
            assign_role(instance, 'recepcionista')
        elif instance.cargo == "G":
            assign_role(instance, 'gerente')
        elif instance.cargo == 'M':
            assign_role(instance, 'medico')