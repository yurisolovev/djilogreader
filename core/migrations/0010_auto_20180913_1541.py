# Generated by Django 2.1 on 2018-09-13 12:41

import core.utils
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0009_note'),
    ]

    operations = [
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('log_file', models.FileField(max_length=128, upload_to=core.utils.log_upload_to, verbose_name='Лог-файл')),
                ('kml_file', models.FileField(blank=True, default='', max_length=128, null=True, upload_to='', verbose_name='Cгенерированный KML')),
                ('csv_file', models.FileField(blank=True, default='', max_length=128, null=True, upload_to='', verbose_name='Сгенерированный CSV')),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата создания')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterField(
            model_name='note',
            name='body',
            field=models.CharField(max_length=1024, verbose_name='Содержание'),
        ),
        migrations.AlterField(
            model_name='note',
            name='title',
            field=models.CharField(max_length=30, verbose_name='Название'),
        ),
    ]