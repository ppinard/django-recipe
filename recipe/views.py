""""""

# Standard library modules.
import re

# Third party modules.
from django.http import JsonResponse, HttpResponseRedirect
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from login_otp.admin import UserAuthenticationForm
from bs4 import BeautifulSoup
import markdown

# Local modules.
from .models import Recipe
from .processor import MARKDOWN_EXT_PREVIEW
from .forms import RecipeCreationForm, RecipeChangeForm

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


class RecipeListView(RecipeBaseMixin, ListView):
    template_name = "recipe/recipe_list.html"
    model = Recipe
    paginate_by = 25
    context_object_name = "recipes"

    def get_queryset(self):
        category = self.kwargs["category"]
        return self.model.objects.filter(category=category)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        category = self.kwargs["category"]
        context["requested_category_key"] = category
        context["requested_category_name"] = dict(context["categories"])[category]

        return context


class RecipeDetailsView(RecipeBaseMixin, TemplateView):
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


class RecipeCreateView(RecipeBaseMixin, LoginRequiredMixin, CreateView):
    template_name = "recipe/recipe_create.html"
    form_class = RecipeCreationForm
    success_url = "/"

    def form_valid(self, form):
        form.instance.user = self.request.user
        super().form_valid(form)

        pk = self.object.pk
        return HttpResponseRedirect(f"/recipe/{pk}/")


class RecipeChangeView(RecipeBaseMixin, UserPassesTestMixin, UpdateView):
    template_name = "recipe/recipe_change.html"
    model = Recipe
    form_class = RecipeChangeForm
    success_url = "/"

    def get_queryset(self):
        pk = self.kwargs["pk"]
        return self.model.objects.filter(pk=pk)

    def test_func(self):
        obj = self.get_object()
        return self.request.user.is_admin or obj.user == self.request.user

    def form_valid(self, form):
        super().form_valid(form)

        pk = self.object.pk
        return HttpResponseRedirect(f"/recipe/{pk}/")


def process_instructions(request):
    rawcontent = request.GET["content"]
    outcontent = markdown.markdown(
        rawcontent, output="html5", extensions=[MARKDOWN_EXT_PREVIEW]
    )
    return JsonResponse({"content": outcontent})
