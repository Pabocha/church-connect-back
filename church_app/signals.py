from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Annonces, Programmes, Notifications
from django.contrib.auth import get_user_model

User = get_user_model()

@receiver(post_save, sender=Annonces)
def create_annonce_notification(sender, instance, created, **kwargs):
    if created:
        # Notifier les utilisateurs lorsque qu'une nouvelle annonce est ajoutée
        users = User.objects.all()  # Par exemple, notifier tous les utilisateurs
        for user in users:
            Notifications.objects.create(
                user=user,
                title = instance.titre,
                message=f"{instance.message}",
                type_notif = 'annonce',
                annonce=instance
            )

@receiver(post_save, sender=Programmes)
def create_programme_notification(sender, instance, created, **kwargs):
    if created:
        # Notifier les utilisateurs lorsque qu'un nouveau programme est ajouté
        users = User.objects.all()  # Par exemple, notifier tous les utilisateurs
        for user in users:
            Notifications.objects.create(
                user=user,
                title = instance.titre,
                message=f"{instance.message}",
                type_notif = 'programme',
                programme=instance
            )
