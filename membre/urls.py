from django.urls import path

from . import views


app_name = "membre"


urlpatterns = [
    path(
        "",
        views.liste_medias,
        name="liste_medias",
    ),
]