# Generated by Django 5.1 on 2024-08-21 12:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('english_words_app', '0003_alter_word_data_alter_word_ru_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='favorites',
            field=models.ManyToManyField(related_name='favorites', to='english_words_app.word'),
        ),
    ]
