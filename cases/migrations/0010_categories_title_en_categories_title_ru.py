# Generated by Django 4.0.5 on 2022-09-23 07:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cases', '0009_remove_case_status_en_remove_case_status_ru'),
    ]

    operations = [
        migrations.AddField(
            model_name='categories',
            name='title_en',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='categories',
            name='title_ru',
            field=models.CharField(max_length=255, null=True),
        ),
    ]