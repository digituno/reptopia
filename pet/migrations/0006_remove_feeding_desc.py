# Generated by Django 3.0.2 on 2020-03-11 04:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pet', '0005_auto_20200311_1353'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='feeding',
            name='desc',
        ),
    ]
