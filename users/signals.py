from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group
from .models import Usuario


@receiver(post_save, sender=Usuario)
def assign_user_to_groups(sender, instance, created, **kwargs):
    grupos = {
        "Jugadores": Group.objects.get_or_create(name="Jugadores")[0],
        "Arbitros": Group.objects.get_or_create(name="Arbitros")[0],
        "Administradores": Group.objects.get_or_create(name="Administradores")[0],
    }

    instance.groups.clear()

    if instance.es_admin_aso:
        instance.groups.add(grupos["Administradores"])
    elif instance.es_arbitro:
        instance.groups.add(grupos["Arbitros"])
    else:
        instance.groups.add(grupos["Jugadores"])

    if (
        instance.is_superuser
        and not instance.groups.filter(name="Administradores").exists()
    ):
        instance.groups.add(grupos["Administradores"])
