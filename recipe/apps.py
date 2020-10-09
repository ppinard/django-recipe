""""""

# Standard library modules.

# Third party modules.
from django.apps import AppConfig
import markdown

# Local modules.
from .processor import RecipeExtension

# Globals and constants variables.


class RecipeConfig(AppConfig):
    name = "recipe"

    unit_definitions = {
        "mL": {"digits": 0},
        "g": {"digits": 0},
        "tablespoon": {"min": 0.0, "max": 10.0, "digits": 2},
        "teaspoon": {"min": 0.0, "max": 10.0, "digits": 2},
        "cup": {"min": 0.0, "max": 10.0, "digits": 1},
    }
    unit_conversions = [
        {
            "names": ["water", "milk"],
            "density": 1.0,
            "units": ["mL", "cup", "g", "tablespoon", "teaspoon"],
        },
        {
            "names": ["flour"],
            "density": 0.528344104716297,
            "units": ["cup", "g", "tablespoon", "teaspoon"],
        },
        {
            "names": ["sugar", "brown sugar", "granulated sugar"],
            "density": 0.8453505675460752,
            "units": ["cup", "g", "tablespoon", "teaspoon"],
        },
        {
            "names": ["butter"],
            "density": 0.9594728941647953,
            "units": ["cup", "g", "tablespoon", "teaspoon"],
        },
        {
            "names": ["oil", "vegetable oil", "olive oil", "sunflower oil"],
            "density": 0.918,
            "units": ["mL", "cup", "g", "tablespoon", "teaspoon"],
        },
        {
            "names": ["tomato passata", "tomato sauce"],
            "density": 1.0355182768975872,
            "units": ["mL", "cup", "g", "tablespoon", "teaspoon"],
        },
        {
            "names": ["bulgur"],
            "density": 0.59,
            "units": ["cup", "g", "tablespoon", "teaspoon"],
        },
    ]

    def ready(self):
        super().ready()
        self.ext = RecipeExtension(self.unit_definitions, self.unit_conversions)

    def process_recipe_instructions(self, rawcontent):
        return markdown.markdown(rawcontent, output="html5", extensions=[self.ext])
