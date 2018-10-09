from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import HStoreField
from django.dispatch import receiver
from django.utils import timezone

from django_countries.fields import CountryField
from sorl.thumbnail import ImageField

from .utils import profile_photo_upload_to as profile_path
from .utils import log_upload_to as log_path
from .utils import DjiLogParser, get_data, delete_dir


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_photo = ImageField(upload_to=profile_path, verbose_name='Фото профиля', blank=True, null=True)
    info = models.TextField('О себе', blank=True, null=True, default='')
    dron_model = models.CharField('Модель DJI', max_length=150)
    birthdate = models.DateField(blank=True, null=True, verbose_name='Дата рождения')
    country = CountryField(blank_label='(не выбрано)', verbose_name='Страна')

    class Meta:
        verbose_name = 'Профиль'

    def __str__(self):
        return self.user.username


class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField('Название', max_length=30)
    body = models.CharField('Содержание', max_length=1024)
    timestamp = models.DateTimeField(default=timezone.now, verbose_name='Дата создания')

    class Meta:
        verbose_name = 'Заметка'
        verbose_name_plural = 'Заметки'

    def __str__(self):
        return '{}: {}'.format(self.title[:15], self.body[:30])


class Log(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    log_file = models.FileField(verbose_name='Лог-файл', upload_to=log_path, max_length=256)
    kml_file = models.FileField(verbose_name='Cгенерированный KML', default='', max_length=256, blank=True)
    gpx_file = models.FileField(verbose_name='Cгенерированный GPX', default='', max_length=256, blank=True)
    csv_file = models.FileField(verbose_name='Сгенерированный CSV', default='', max_length=256, blank=True)
    log_directory = models.CharField(verbose_name='Путь к каталогу лога', default='', max_length=256, blank=True)
    data = HStoreField(default=dict)
    start_time = models.DateTimeField(verbose_name='Время начала полета', blank=True, null=True)
    end_time = models.DateTimeField(verbose_name='Время окончания полета', blank=True, null=True)
    timestamp = models.DateTimeField(default=timezone.now, verbose_name='Дата создания')

    class Meta:
        verbose_name = 'Полетный лог'
        verbose_name_plural = 'Полетные логи'

    def __str__(self):
        return 'Полетный лог-файл: {}'.format(self.log_file.name)

    def create_csv_gpx(self):
        parser = DjiLogParser(self)
        if not parser.create_all():
            self.delete()
        else:
            get_data(self)

    def delete_log_files(self):
        delete_dir(self.log_directory)


@receiver(models.signals.post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """ Create Profile object when User was created """
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


@receiver(models.signals.post_save, sender=Log)
def create_csv_gpx(sender, instance, created, **kwargs):
    """ Parse uploaded DJI log-file when Log was created"""
    if created:
        instance.create_csv_gpx()
