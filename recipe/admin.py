""""""

# Standard library modules.

# Third party modules.
from django.contrib import admin

# Local modules.
from .models import Recipe
from .forms import AdminRecipeCreationForm, AdminRecipeChangeForm

# Globals and constants variables.


class RecipeAdmin(admin.ModelAdmin):
    # The forms to add and change user instances
    form = AdminRecipeChangeForm
    add_form = AdminRecipeCreationForm

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
