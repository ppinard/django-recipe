""""""

# Standard library modules.
import re

# Third party modules.
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.contrib.auth import views as auth_views
from login_otp.admin import UserAuthenticationForm
from bs4 import BeautifulSoup

# Local modules.
from .models import Recipe

# Globals and constants variables.


class RecipeBaseMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = list(
            Recipe.RecipeCategory.choices  # @UndefinedVariable
        )
        return context


class LoginView(RecipeBaseMixin, auth_views.LoginView):
    form_class = UserAuthenticationForm
    template_name = "recipe/login.html"


class LogoutView(RecipeBaseMixin, auth_views.LogoutView):
    template_name = "recipe/logout.html"


class RecipeIndexView(RecipeBaseMixin, TemplateView):
    template_name = "recipe/home.html"


class RecipeCategoryListView(RecipeBaseMixin, ListView):
    template_name = "recipe/recipe_list.html"
    model = Recipe
    paginate_by = 5

    def get_queryset(self):
        category = self.kwargs["category"]
        return self.model.objects.filter(category=category)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        category = self.kwargs["category"]
        context["requested_category_key"] = category
        context["requested_category_name"] = dict(context["categories"])[category]

        return context


class RecipeView(RecipeBaseMixin, TemplateView):
    template_name = "recipe/recipe_view.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["recipe"] = recipe = Recipe.objects.get(pk=self.kwargs["pk"])
        context["requested_category_key"] = recipe.category

        # Change heading level
        heading_top = 3
        content = recipe.instructions_html
        soup = BeautifulSoup(content, "html.parser")
        pattern = re.compile(r"^h(\d)$")
        for tag in soup.find_all(pattern):
            tag.name = "h%d" % (int(pattern.match(tag.name).group(1)) - 1 + heading_top)

        context["instructions_html"] = str(soup)

        return context
