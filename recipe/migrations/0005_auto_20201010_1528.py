# Generated by Django 3.1.2 on 2020-10-10 19:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0004_auto_20201010_1514'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='instructions_markdown',
            field=models.TextField(help_text='Enter instructions for the recipe. Enter ingredient as <code>[quantity](unit)[ingredient]</code>\nor <code>[quantity][ingredient]</code>. The ingredient list will be\nautomatically compiled from the ingredients in the instructions.\nEnter temperature as (<code>temperature)[C]</code> or <code>(temperature)[F]</code>\n', verbose_name='instructions'),
        ),
    ]
