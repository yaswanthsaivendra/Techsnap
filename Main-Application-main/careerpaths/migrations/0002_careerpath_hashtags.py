# Generated by Django 3.2.6 on 2022-12-28 20:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hashtags', '0001_initial'),
        ('careerpaths', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='careerpath',
            name='hashtags',
            field=models.ManyToManyField(blank=True, to='hashtags.Hashtag'),
        ),
    ]
