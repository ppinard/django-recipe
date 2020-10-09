# Generated by Django 3.1.2 on 2020-10-08 17:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='cooking_time_min',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='recipe',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='recipe',
            name='image',
            field=models.BinaryField(null=True),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='category',
            field=models.CharField(choices=[('soup', 'Soup'), ('bread', 'Bread'), ('fish', 'Fish'), ('meat', 'Meat'), ('pasta', 'Pasta'), ('sidedish', 'Side dish'), ('dessert', 'Dessert'), ('breakfast', 'Breakfast')], max_length=255, verbose_name='category'),
        ),
    ]
