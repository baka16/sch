# Generated by Django 2.2.7 on 2019-11-30 18:36

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('aids', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='schoolinfo',
            old_name='short_name',
            new_name='title',
        ),
        migrations.RemoveField(
            model_name='classroom',
            name='class_slug',
        ),
        migrations.RemoveField(
            model_name='classroom',
            name='short_name',
        ),
        migrations.AddField(
            model_name='classroom',
            name='slug',
            field=models.SlugField(default=django.utils.timezone.now, help_text='Unique class name without spaces', unique=True, verbose_name='Class Slug'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='classroom',
            name='title',
            field=models.CharField(default=django.utils.timezone.now, help_text='Enter class short name', max_length=20),
            preserve_default=False,
        ),
    ]