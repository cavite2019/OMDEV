# Generated by Django 2.2 on 2019-10-09 00:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('domain', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='domain_c',
            name='output',
        ),
    ]
