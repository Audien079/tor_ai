# Generated by Django 4.2.1 on 2024-12-07 08:32

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_userip_searchlog'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='searchlog',
            name='search_term',
        ),
        migrations.RemoveField(
            model_name='searchlog',
            name='timestamp',
        ),
        migrations.AddField(
            model_name='searchlog',
            name='keyword',
            field=models.CharField(default=0, max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='searchlog',
            name='last_searched',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]