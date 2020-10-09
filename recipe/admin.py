""""""

# Standard library modules.

# Third party modules.
from django import forms
from django.contrib import admin

# Local modules.
from .models import Recipe

# Globals and constants variables.


class RecipeCreationForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = (
            "category",
            "name",
            "description",
            "user",
            "reference",
            "cooking_time_min",
            "instructions_markdown",
            "image",
        )


class RecipeChangeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = (
            "category",
            "name",
            "description",
            "user",
            "reference",
            "cooking_time_min",
            "instructions_markdown",
            "image",
        )


class RecipeAdmin(admin.ModelAdmin):
    # The forms to add and change user instances
    form = RecipeChangeForm
    add_form = RecipeCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ("name", "category", "description", "user")
    list_filter = ()
    fieldsets = (
        (
            "Info",
            {"fields": ("category", "name", "description", "user", "reference",)},
        ),
        (
            "Instructions",
            {"fields": ("cooking_time_min", "instructions_markdown", "image")},
        ),
    )
    #     # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    #     # overrides get_fieldsets to use this attribute when creating a user.
    #     add_fieldsets = (
    #         ("Info", {"fields": ("category", "name", "user", "reference")}),
    #         ("Instructions", {"fields": ("instructions_markdown",)}),
    #     )
    search_fields = ("category", "name")
    ordering = ("category", "name")
    filter_horizontal = ()


admin.site.register(Recipe, RecipeAdmin)
