# Generated by Django 3.2.6 on 2022-12-28 20:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='blogs',
            old_name='tags',
            new_name='hashtags',
        ),
    ]
