# Generated by Django 4.0.5 on 2022-09-23 09:17

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('username', models.CharField(blank=True, max_length=50)),
                ('second_name', models.CharField(blank=True, max_length=50)),
                ('email', models.EmailField(max_length=254, primary_key=True, serialize=False)),
                ('phone_number', models.CharField(blank=True, max_length=15)),
                ('is_active', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('activation_code', models.CharField(blank=True, max_length=5)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
