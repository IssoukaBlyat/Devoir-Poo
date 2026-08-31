from django.urls import path

from . import views


app_name = "bibliothecaire"


urlpatterns = [
    path(
        "",
        views.tableau_bord,
        name="tableau_bord",
    ),

    path(
        "membres/",
        views.liste_membres,
        name="liste_membres",
    ),

    path(
        "membres/ajouter/",
        views.creer_membre,
        name="creer_membre",
    ),

    path(
        "membres/<int:membre_id>/modifier/",
        views.modifier_membre,
        name="modifier_membre",
    ),

    path(
        "membres/<int:membre_id>/supprimer/",
        views.supprimer_membre,
        name="supprimer_membre",
    ),

    path(
        "medias/",
        views.liste_medias,
        name="liste_medias",
    ),

    path(
        "medias/ajouter/livre/",
        views.ajouter_livre,
        name="ajouter_livre",
    ),

    path(
        "medias/ajouter/dvd/",
        views.ajouter_dvd,
        name="ajouter_dvd",
    ),

    path(
        "medias/ajouter/cd/",
        views.ajouter_cd,
        name="ajouter_cd",
    ),

    path(
        "medias/ajouter/jeu/",
        views.ajouter_jeu,
        name="ajouter_jeu",
    ),

    path(
        "emprunts/",
        views.liste_emprunts,
        name="liste_emprunts",
    ),

    path(
        "emprunts/ajouter/",
        views.ajouter_emprunt,
        name="ajouter_emprunt",
    ),

    path(
        "emprunts/<int:emprunt_id>/retour/",
        views.retour_emprunt,
        name="retour_emprunt",
    ),
]