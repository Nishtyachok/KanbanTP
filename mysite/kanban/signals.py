from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Team, Project


@receiver(post_save, sender=Project)
def create_team(sender, instance, created, **kwargs):
    if created:
        t = Team(project=instance)
        t.save()
        t.members.add(instance.owner)

