# Generated by Django 3.2.6 on 2022-11-30 15:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hashtags', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hashtag',
            name='tag',
        ),
        migrations.AddField(
            model_name='hashtag',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='hashtag',
            name='title',
            field=models.CharField(default='python', max_length=100, verbose_name='hashtag name'),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(choices=[('IP', 'Intellectual Property Violation'), ('VODO', 'Violence or Dangerous organizations'), ('BOH', 'Bullying or Harassment')], max_length=200)),
                ('hashtag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hashtags.hashtag')),
            ],
        ),
    ]
