# Generated by Django 3.1.3 on 2020-11-22 18:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0006_recipe_portions'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='category',
            field=models.CharField(choices=[('soup', 'Soup'), ('bread', 'Bread'), ('fish', 'Fish'), ('meat', 'Meat'), ('italian', 'Italian'), ('vegetarian', 'Veg'), ('sidedish', 'Side dish'), ('dessert', 'Dessert'), ('breakfast', 'Breakfast')], max_length=255, verbose_name='category'),
        ),
    ]
