""""""

# Standard library modules.
import uuid
from pathlib import Path

# Third party modules.
from django.db import models
from django.apps import apps
from django.contrib.auth import get_user_model
from cropperjs.models import CropperImageField
import markdown

# Local modules.

# Globals and constants variables.


class Recipe(models.Model):
    class RecipeCategory(models.TextChoices):
        SOUP = "soup", "Soup"
        BREAD = "bread", "Bread"
        FISH = "fish", "Fish"
        MEAT = "meat", "Meat"
        PASTA = "pasta", "Pasta"
        SIDEDISH = "sidedish", "Side dish"
        DESSERT = "dessert", "Dessert"
        BREAKFAST = "breakfast", "Breakfast"

    class Meta:
        ordering = ["name"]

    category = models.CharField(
        "category", max_length=255, choices=RecipeCategory.choices
    )
    name = models.CharField("name", max_length=255)
    description = models.TextField(blank=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True)
    reference = models.CharField("reference", max_length=255, blank=True)
    cooking_time_min = models.PositiveIntegerField(null=True, blank=True)
    image = CropperImageField(
        upload_to=lambda _instance, filename: f"recipe/{uuid.uuid4()}{Path(filename).suffix}",
        null=True,
        blank=True,
        aspectratio=1.0,
        dimensions=(75, 75),
    )
    instructions_markdown = models.TextField("instructions")
    instructions_html = models.TextField(blank=True)

    def __str__(self):
        return f"<Recipe({self.category}-{self.name})>"

    def save(self, *args, **kwargs):
        self.instructions_html = self.process_recipe_instructions(
            self.instructions_markdown,
        )
        super().save(*args, **kwargs)

    def process_recipe_instructions(self, rawcontent):
        config = apps.get_app_config("recipe")
        ext = config.ext
        return markdown.markdown(rawcontent, output="html5", extensions=[ext])
