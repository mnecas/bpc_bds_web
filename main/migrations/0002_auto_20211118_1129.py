# Generated by Django 3.2.9 on 2021-11-18 11:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='person',
            name='passowrd',
        ),
        migrations.AddField(
            model_name='person',
            name='password',
            field=models.CharField(default='', max_length=64),
            preserve_default=False,
        ),
    ]