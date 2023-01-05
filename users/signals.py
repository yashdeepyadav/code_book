from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver
from .models import Profile
from django.contrib.auth.models import User

# Orthodox Method

def save_profile(sender,instance,created,**kwargs):
    print("Profile saved --called from users.singnal ORTHODOX")

post_save.connect(save_profile,sender=Profile)


@receiver(post_save,sender=Profile)
def updateUser(sender,instance,created,**kwargs):
    profile=instance
    user=profile.user

    if created== False:
        user.first_name=profile.name
        user.username=profile.username
        user.email=profile.email
        user.save()

    

@receiver(post_delete,sender=User)
def deleteProfile(sender,instance,**kwargs):
    user=instance
    profile=user.user

    if user:
        user.delete()



@receiver(post_save,sender=User)
def createProfile(sender,instance,created,**kwargs):

    user=instance

    if created:
        Profile.objects.create(
            user=instance,
            username=user.username
        )
        print("Profile created --called from users.singnal DECORATOR")