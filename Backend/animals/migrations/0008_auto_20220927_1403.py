# Generated by Django 3.2.12 on 2022-09-27 14:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('animals', '0007_rename_characteristics_animal_features'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_animal',
            name='playing_cnt',
            field=models.IntegerField(default=5),
        ),
        migrations.AlterField(
            model_name='user_animal',
            name='talking_cnt',
            field=models.IntegerField(default=5),
        ),
    ]
