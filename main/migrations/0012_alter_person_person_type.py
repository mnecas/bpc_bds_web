# Generated by Django 3.2.9 on 2021-11-25 13:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_auto_20211125_1320'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='person_type',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='main.persontype'),
        ),
    ]
