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
        "category/<str:category>/",
        views.RecipeCategoryListView.as_view(),
        name="category",
    ),
    path("recipe/<int:pk>/", views.RecipeView.as_view(), name="recipe"),
    path("login/", views.LoginView.as_view(), name="login",),
    path("logout/", views.LogoutView.as_view(), name="logout"),
]
