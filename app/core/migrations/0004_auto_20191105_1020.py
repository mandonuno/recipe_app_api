# Generated by Django 2.1.9 on 2019-11-05 10:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_ingredients'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Ingredients',
            new_name='Ingredient',
        ),
    ]