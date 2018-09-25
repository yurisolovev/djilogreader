# Generated by Django 2.1 on 2018-09-03 08:49

from django.db import migrations, models
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='profile',
            options={'verbose_name': 'Профиль'},
        ),
        migrations.AddField(
            model_name='profile',
            name='birthdate',
            field=models.DateField(blank=True, null=True, verbose_name='birthdate'),
        ),
        migrations.AddField(
            model_name='profile',
            name='country',
            field=django_countries.fields.CountryField(default=None, max_length=2),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='profile',
            name='aboutme',
            field=models.TextField(verbose_name='Обо мне'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='dron_model',
            field=models.CharField(max_length=150, verbose_name='Модель DJI'),
        ),
    ]
