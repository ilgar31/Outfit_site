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


class Items(models.Model):
    name = models.CharField("Имя товара", max_length=45, blank=True)
    type = models.CharField("Тип", max_length=35, blank=True)
    size = models.CharField("Доступные размеры", max_length=35, blank=True)
    cost = models.IntegerField("Стоимость", blank=True)
    GENDER_CHOICES = (('M', 'Мужской'), ('F', 'Женский'))
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    brand = models.CharField("Бренд", max_length=40, blank=True)
    color = models.CharField("Цвет", max_length=20, blank=True)
    description = models.TextField("Описание", blank=True)

    def __str__(self):
        return f'{self.name} ({self.color})'

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

