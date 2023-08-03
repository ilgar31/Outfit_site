from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime


def png_save(instance, filename):
    return f'main/png/users/user_{instance.id} ({instance.user.username})/{filename}'


def img_save(instance, filename):
    return f'main/png/items/item_{instance.item.id}/{filename}'


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


class Item_images(models.Model):
    item = models.ForeignKey(Items, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to=img_save)

    def __str__(self):
        return f'{self.image}'


class Item_sizes(models.Model):
    item = models.ForeignKey(Items, on_delete=models.CASCADE, related_name="sizes")
    type_size = models.CharField("Тип размера (страна)", blank=True, max_length=10)
    size = models.CharField("Размер", blank=True, max_length=10)

    def __str__(self):
        return f'{self.type_size}-{self.size}'


class Favorites(models.Model):
    id_user = models.IntegerField("ID пользователя", blank=True)
    id_item = models.IntegerField("ID товара", blank=True)

    def __str__(self):
        return f"{self.id_user} -> {self.id_item}"

    class Meta:
        verbose_name = "Избранное"
        verbose_name_plural = "Избранное"


class Basket(models.Model):
    id_user = models.IntegerField("ID пользователя", blank=True)
    id_item = models.IntegerField("ID товара", blank=True)
    item_type_size = models.CharField("Тип размера (страна)", blank=True, max_length=10)
    item_size = models.CharField("Размер", blank=True, max_length=10)
    count = models.IntegerField("Количество", default=1, blank=True)

    def __str__(self):
        return f"{self.id_user} -> {self.id_item} ({self.item_type_size}-{self.item_size})"

    class Meta:
        verbose_name = "Корзина"
        verbose_name_plural = "Корзина"


class Purchase(models.Model):
    id_user = models.IntegerField("ID пользователя", blank=True)
    offer_number = models.CharField("Номер заказа", blank=True, max_length=50)
    number = models.CharField("Мобильный номер", blank=True, max_length=50)
    FIO = models.CharField("ФИО", blank=True, max_length=50)
    tg = models.CharField("Телеграм", blank=True, max_length=50)
    email = models.CharField("Почта", blank=True, max_length=50)
    region = models.CharField("Регион", blank=True, max_length=50)
    city = models.CharField("Город", blank=True, max_length=50)
    delivery = models.CharField("Тип доставки", blank=True, max_length=50)
    payment = models.CharField("Тип оплаты", blank=True, max_length=50)
    date = models.DateTimeField("Дата и время покупки", default=datetime.now, blank=True)
    step = models.CharField("Стадия заказа", blank=True, max_length=50, default="Принят")

    def __str__(self):
        return f"{self.id_user} -> {self.offer_number}"

    class Meta:
        verbose_name = "Покупка"
        verbose_name_plural = "Покупки"


class Items_purchase(models.Model):
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE, related_name="items")
    id_item = models.IntegerField("ID товара", blank=True)
    item_type_size = models.CharField("Тип размера (страна)", blank=True, max_length=10)
    item_size = models.CharField("Размер", blank=True, max_length=10)
    count = models.IntegerField("Количество", default=1, blank=True)

    def __str__(self):
        return f'{self.id_item}'
