# Generated by Django 3.0.2 on 2020-02-08 08:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pet', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pet',
            old_name='user',
            new_name='owner',
        ),
    ]