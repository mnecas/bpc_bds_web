# Generated by Django 3.2.9 on 2021-11-25 13:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_person_email'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='person',
            name='email',
        ),
        migrations.AlterModelTable(
            name='person',
            table='galaxy_user',
        ),
    ]