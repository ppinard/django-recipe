""""""

# Standard library modules.

# Third party modules.
from django.urls import path

# Local modules.
from . import views

# Globals and constants variables.


urlpatterns = [
    path("", views.RecipeIndexView.as_view(), name="index"),
    path(
        "category/<str:category>/", views.RecipeListView.as_view(), name="recipe-list",
    ),
    path("recipe/<int:pk>/", views.RecipeDetailsView.as_view(), name="recipe-details"),
    path("recipe/create/", views.RecipeCreateView.as_view(), name="recipe-create"),
    path(
        "recipe/<int:pk>/change/",
        views.RecipeChangeView.as_view(),
        name="recipe-change",
    ),
    path("api/process", views.process_instructions, name="process"),
    path("login/", views.LoginView.as_view(), name="login",),
    path("logout/", views.LogoutView.as_view(), name="logout"),
]
