# Generated by Django 3.0.2 on 2020-03-11 04:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dict', '0001_initial'),
        ('pet', '0004_pet_created_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='feeding',
            name='desc',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='feeding',
            name='eat_type',
            field=models.ForeignKey(default=21, on_delete=django.db.models.deletion.CASCADE, related_name='eat_type', to='dict.Dictionary'),
        ),
        migrations.AlterField(
            model_name='feeding',
            name='prey_size',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='prey_size', to='dict.Dictionary'),
        ),
    ]
