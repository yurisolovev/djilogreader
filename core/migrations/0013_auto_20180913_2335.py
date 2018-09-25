# Generated by Django 2.1 on 2018-09-13 20:35

import core.utils
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_auto_20180913_2333'),
    ]

    operations = [
        migrations.AlterField(
            model_name='log',
            name='csv_file',
            field=models.FileField(blank=True, default='', max_length=256, upload_to='', verbose_name='Сгенерированный CSV'),
        ),
        migrations.AlterField(
            model_name='log',
            name='kml_file',
            field=models.FileField(blank=True, default='', max_length=256, upload_to='', verbose_name='Cгенерированный KML'),
        ),
        migrations.AlterField(
            model_name='log',
            name='log_directory',
            field=models.CharField(blank=True, default='', max_length=256, verbose_name='Путь к каталогу лога'),
        ),
        migrations.AlterField(
            model_name='log',
            name='log_file',
            field=models.FileField(max_length=256, upload_to=core.utils.log_upload_to, verbose_name='Лог-файл'),
        ),
    ]
