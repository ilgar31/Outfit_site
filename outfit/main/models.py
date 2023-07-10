from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


def png_save(instance, filename):
    return f'main/png/users/user_{instance.id} ({instance.user.username})/{filename}'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_name = models.CharField("Имя", max_length=25, blank=True)
    user_surname = models.CharField("Фамилия", max_length=25, blank=True)
    img = models.FileField("Фотография", upload_to=png_save, blank=True)
    birthday = models.DateField("День рождения", null=True, blank=True)
    gender = models.BooleanField('Пол', default=0, max_length=20, blank=True)
    country = models.CharField("Город", max_length=40, blank=True)

    def __str__(self):
        if self.user_name:
            if self.user_surname:
                return f"{self.user_name} {self.user_surname}"
            else:
                return f"{self.user_name}"
        return self.user.username

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

