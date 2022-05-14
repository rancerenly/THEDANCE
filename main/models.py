from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.contrib.auth.models import User


class TeacherProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='teacher_profile')
    education_certificate = models.PositiveIntegerField(verbose_name='Сертификат', unique=True, blank=True)
    profession = models.CharField(max_length=100, verbose_name='Профессия', blank=True)
    home = models.CharField(max_length=200, verbose_name='Адрес', blank=True)

    class Meta:
        verbose_name_plural = 'Учителя'
        verbose_name = 'Учитель'
        ordering = ['profession', 'user']

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse('teacher', kwargs={'id': self.id})


class ClientProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    passport = models.CharField(max_length=12, help_text='Пример: 1234 567890', verbose_name='Паспортные данные',)
    phone = models.CharField(max_length=13, verbose_name='Номер телефона')

    class Meta:
        verbose_name_plural = 'Клиенты'
        verbose_name = 'Клиент'
        indexes = [
            models.Index(fields=['user'])  # быстрый поиск
            # с помощью индексов
        ]

    def __str__(self):
        return self.user.first_name

    @receiver(post_save, sender=User)
    def update_user_profile(sender, instance, created, **kwargs):
        if created:
            print(instance)
            ClientProfile.objects.create(user=instance)
        instance.profile.save()

    def get_absolute_url(self):
        return reverse('client', kwargs={'id': self.id})


class Style(models.Model):
    name = models.CharField(max_length=50)
    teacher = models.ForeignKey(TeacherProfile, on_delete=models.SET_NULL, null=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='Цена')
    description = models.TextField(verbose_name='Описание')
    clients = models.ManyToManyField(ClientProfile)

    class Meta:
        verbose_name_plural = 'Предметы'
        verbose_name = 'Предмет'

    def __str__(self):
        return self.name


class Schedule(models.Model):
    style = models.ForeignKey(Style, on_delete=models.CASCADE, verbose_name='Название предмета')
    weekday = models.CharField(max_length=2, verbose_name='День недели')
    time = models.TimeField(verbose_name='Время проведения')

    class Meta:
        verbose_name_plural = 'Расписания'
        verbose_name = 'Расписание'
        ordering = ['weekday', 'time']


class Payment(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Клиент')
    cost = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='Стоимость')
    payment_date = models.DateField(verbose_name='Дата платежа')

    class Meta:
        verbose_name_plural = 'Чеки'
        verbose_name = 'Чек'
        ordering = ['payment_date']  # Сортировка
        get_latest_by = 'payment_date'  # latest() - получить ближайшую дату
        indexes = [
            models.Index(fields=['client'])
        ]
