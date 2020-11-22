""""""

# Standard library modules.

# Third party modules.
from django.core.management.base import BaseCommand
from django.conf import settings
from loguru import logger
import markdown
import tabulate

# Local modules.
from recipe.processor import RecipeExtension
from recipe.models import Recipe

# Globals and constants variables.


class Command(BaseCommand):
    help = "Search missing unit definitions"

    def handle(self, *args, **options):
        markdown_ext = RecipeExtension(
            getattr(settings, "RECIPE_UNIT_DEFINITIONS", {}),
            getattr(settings, "RECIPE_UNIT_CONVERSIONS", []),
            output_ingredient_list=False,
        )

        logger.remove()

        # Collect errors
        errors = {}
        for model in Recipe.objects.all():
            rawcontent = model.instructions_markdown
            markdown.markdown(rawcontent, output="html5", extensions=[markdown_ext])

            for error in markdown_ext.recipe_processor.ingredientlist.errors:
                error_type = type(error).__name__
                errors.setdefault(error_type, [])
                errors[error_type].append((model.pk, model.name, str(error)))

        # Print in categories
        for error_type in sorted(errors):
            print("=" * 80)
            print(error_type)
            print("-" * len(error_type))
            print(
                tabulate.tabulate(
                    sorted(errors[error_type]), headers=["id", "recipe", "error"]
                )
            )
