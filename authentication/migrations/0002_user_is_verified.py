# Generated by Django 5.1 on 2024-08-13 10:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_verified',
            field=models.BooleanField(default=False, verbose_name='Is Verified'),
        ),
    ]
