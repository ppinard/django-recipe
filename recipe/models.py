""""""

# Standard library modules.
import uuid
from pathlib import Path

# Third party modules.
from django.db import models
from django.contrib.auth import get_user_model
from cropperjs.models import CropperImageField
import markdown

# Local modules.
from .processor import MARKDOWN_EXT

# Globals and constants variables.


def _recipe_upload_to(instance, filename):
    return f"recipe/{uuid.uuid4()}{Path(filename).suffix}"


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
        upload_to=_recipe_upload_to,
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
        return markdown.markdown(rawcontent, output="html5", extensions=[MARKDOWN_EXT])
