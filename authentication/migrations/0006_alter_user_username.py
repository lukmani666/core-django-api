# Generated by Django 5.1 on 2024-08-15 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0005_alter_user_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(blank=True, max_length=50, unique=True, verbose_name='Username'),
        ),
    ]
