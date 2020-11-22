""""""

# Standard library modules.

# Third party modules.
from django.core.management.base import BaseCommand
import markdown

# Local modules.
from recipe.processor import MARKDOWN_EXT
from recipe.models import Recipe

# Globals and constants variables.


class Command(BaseCommand):
    help = "Refresh html instructions of recipes"

    def handle(self, *args, **options):
        for model in Recipe.objects.all():
            rawcontent = model.instructions_markdown
            model.instructions_html = markdown.markdown(
                rawcontent, output="html5", extensions=[MARKDOWN_EXT]
            )
            model.save()
