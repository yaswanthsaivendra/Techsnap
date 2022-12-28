# Generated by Django 3.2.6 on 2022-12-28 15:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('email', models.EmailField(max_length=254)),
                ('msg', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Contribute',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('F_name', models.CharField(max_length=200)),
                ('L_name', models.CharField(max_length=200)),
                ('email', models.EmailField(max_length=254)),
                ('linkedin', models.URLField(max_length=300)),
                ('how', models.CharField(max_length=300)),
                ('msg', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='FAQ',
            fields=[
                ('auto_increment_id', models.AutoField(primary_key=True, serialize=False)),
                ('topic', models.CharField(choices=[('Account', 'Account'), ('Enrollment', 'Enrollment'), ('Communication', 'Communication'), ('Certification', 'Certification'), ('Others', 'Others')], default='Others', max_length=50)),
                ('question', models.TextField()),
                ('answer', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='sbu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('F_name', models.CharField(max_length=200)),
                ('L_name', models.CharField(max_length=200)),
                ('email', models.EmailField(max_length=254)),
                ('linkedin', models.URLField(max_length=300)),
                ('how', models.CharField(max_length=300)),
                ('msg', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Storage_Media',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.ImageField(upload_to='storage')),
                ('name', models.CharField(default='logo', max_length=200, unique=True)),
            ],
        ),
    ]
