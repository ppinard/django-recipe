""""""

# Standard library modules.

# Third party modules.
from django import forms
import django.forms.widgets as widgets

# Local modules.\
from .models import Recipe
from .widgets import InstructionsTextWidget

# Globals and constants variables.


class RecipeCreationForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = (
            "category",
            "name",
            "description",
            "reference",
            "cooking_time_min",
            "instructions_markdown",
            "image",
        )
        widgets = {
            "description": widgets.Textarea(attrs={"cols": "40", "rows": "3"}),
            "instructions_markdown": InstructionsTextWidget(),
        }


class AdminRecipeCreationForm(forms.ModelForm):
    class Meta(RecipeCreationForm.Meta):
        fields = RecipeCreationForm.Meta.fields + ("user",)


class RecipeChangeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = (
            "category",
            "name",
            "description",
            "reference",
            "cooking_time_min",
            "instructions_markdown",
            "image",
        )
        widgets = {
            "description": widgets.Textarea(attrs={"cols": "40", "rows": "3"}),
            "instructions_markdown": InstructionsTextWidget(),
        }


class AdminRecipeChangeForm(forms.ModelForm):
    class Meta(RecipeChangeForm.Meta):
        fields = RecipeCreationForm.Meta.fields + ("user",)
