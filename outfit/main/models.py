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
    GENDER_CHOICES = (('M', 'Мужской'), ('F', 'Женский'))
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    country = models.CharField("Город", max_length=40, blank=True)

    def __str__(self):
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

