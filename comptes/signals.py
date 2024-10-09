from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
from .models import GroupProfile
import os

@receiver(post_delete, sender=GroupProfile)
def delete_group_image(sender, instance, **kwargs):
    """Supprime l'image du groupe du système de fichiers après la suppression du groupe."""
    if instance.image:
        # Supprimer l'image du stockage
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)

@receiver(pre_save, sender=GroupProfile)
def delete_old_image_on_update(sender, instance, **kwargs):
    """Supprime l'ancienne image si une nouvelle image est fournie lors de la mise à jour du groupe."""
    if instance.pk:  # Vérifie si l'instance existe déjà (c'est une mise à jour)
        try:
            old_instance = GroupProfile.objects.get(pk=instance.pk)
        except GroupProfile.DoesNotExist:
            return  # L'instance n'existe pas, on ne fait rien

        # Vérifiez si une nouvelle image est fournie et si l'ancienne image est différente
        if instance.image and old_instance.image and instance.image != old_instance.image:
            old_image_path = old_instance.image.path
            if os.path.isfile(old_image_path):
                os.remove(old_image_path)
            
