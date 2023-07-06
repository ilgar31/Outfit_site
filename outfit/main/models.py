from django.db import models


class Users(models.Model):
    email = models.CharField("Электронная почта", max_length=50)
    password = models.CharField("Пароль", max_length=35)
    login = models.CharField("Логин", max_length=40, default='', blank=True)
    user_name = models.CharField("Имя", max_length=25, default='', blank=True)
    user_surname = models.CharField("Фамилия", max_length=25, default='', blank=True)
    img_link = models.URLField("Ссылка на изображение для аватарки", default='', blank=True)
    birthday = models.DateField("День рождения", max_length=25, default='', blank=True)
    gender = models.CharField('Пол', default=0, max_length=20)
    money = models.IntegerField("Баланс", default=0)
    products_purchased = models.IntegerField('Количество купленных товаров', default=0)

    def __str__(self):
        if self.user_name:
            if self.user_surname:
                return f"{self.user_name} {self.user_surname}"
            else:
                return f"{self.user_name}"
        return self.email

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
