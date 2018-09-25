# Generated by Django 2.1 on 2018-09-20 20:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_remove_log_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='log',
            name='end_time',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Время окончания полета'),
        ),
        migrations.AddField(
            model_name='log',
            name='start_time',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Время начала полета'),
        ),
    ]
