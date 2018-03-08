from django.dispatch import receiver
from django.db.models.signals import post_delete, post_save, pre_save
from django.contrib.auth.models import User
from .models import UserProfile

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, created, **kwargs):

    try:
    #if instance.userprofile:
        instance.userprofile.save()
    #else:
    except:
        userprofile = UserProfile.objects.create(user = instance)
        instance.userprofile = userprofile
        instance.userprofile.save()
