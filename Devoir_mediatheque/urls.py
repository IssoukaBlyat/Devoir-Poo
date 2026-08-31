from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path(
        "admin/",
        admin.site.urls,
    ),

    path(
        "bibliothecaire",
        include("bibliothecaire.urls"),
    ),

    path(
        "comptes/",
        include("django.contrib.auth.urls"),
    ),

    path(
        "",
        include("membre.urls"),
    ),
]