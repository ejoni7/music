# Generated by Django 5.0.1 on 2024-01-16 13:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='songpage',
            name='song_image',
            field=models.ImageField(blank=True, upload_to='song_pic'),
        ),
    ]