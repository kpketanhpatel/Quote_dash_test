# Generated by Django 2.2 on 2020-08-24 00:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_one', '0002_auto_20200816_2005'),
    ]

    operations = [
        migrations.AddField(
            model_name='quote',
            name='likes',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='likes_quote', to='app_one.User'),
            preserve_default=False,
        ),
    ]