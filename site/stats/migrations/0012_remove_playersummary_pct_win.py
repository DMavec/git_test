# Generated by Django 2.0.2 on 2018-03-14 03:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0011_auto_20180313_1504'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='playersummary',
            name='pct_win',
        ),
    ]