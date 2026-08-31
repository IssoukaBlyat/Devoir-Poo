import logging

from django.db.models.deletion import ProtectedError

from django.contrib.auth.decorators import user_passes_test

from django.shortcuts import (
    get_object_or_404,
    redirect,
    render,
)

from .forms import (
    CdForm,
    DvdForm,
    EmpruntForm,
    JeuDePlateauForm,
    LivreForm,
    MembreForm,
)

from django.core.exceptions import ValidationError

from .services import (
    creer_emprunt,
    retourner_emprunt,
)

from .models import (
    Cd,
    Dvd,
    Emprunt,
    JeuDePlateau,
    Livre,
    Media,
    Membre,
)

logger = logging.getLogger(__name__)

def est_bibliothecaire(user):
    return user.is_authenticated and user.is_staff

@user_passes_test(est_bibliothecaire)
def tableau_bord(request):
    nombre_membres = Membre.objects.count()
    nombre_medias = (
            Media.objects.count()
            + JeuDePlateau.objects.count()
    )

    return render(
        request,
        "bibliothecaire/tableau_bord.html",
        {
            "nombre_membres": nombre_membres,
            "nombre_medias": nombre_medias,
        },
    )

@user_passes_test(est_bibliothecaire)
def liste_membres(request):
    membres = Membre.objects.all().order_by(
        "nom",
        "prenom",
    )

    return render(
        request,
        "bibliothecaire/liste_membres.html",
        {
            "membres": membres,
        },
    )

@user_passes_test(est_bibliothecaire)
def creer_membre(request):
    if request.method == "POST":
        form = MembreForm(request.POST)

        if form.is_valid():
            membre = form.save()

            logger.info(
                "Création du membre : %s",
                membre,
            )

            return redirect(
                "bibliothecaire:liste_membres"
            )

    else:
        form = MembreForm()

    return render(
        request,
        "bibliothecaire/formulaire_membre.html",
        {
            "form": form,
            "titre": "Ajouter un membre",
        },
    )

@user_passes_test(est_bibliothecaire)
def modifier_membre(request, membre_id):
    membre = get_object_or_404(
        Membre,
        id=membre_id,
    )

    if request.method == "POST":
        form = MembreForm(
            request.POST,
            instance=membre,
        )

        if form.is_valid():
            membre = form.save()

            logger.info(
                "Modification du membre : %s",
                membre,
            )

            return redirect(
                "bibliothecaire:liste_membres"
            )

    else:
        form = MembreForm(
            instance=membre,
        )

    return render(
        request,
        "bibliothecaire/formulaire_membre.html",
        {
            "form": form,
            "titre": "Modifier un membre",
        },
    )

@user_passes_test(est_bibliothecaire)
def supprimer_membre(request, membre_id):
    membre = get_object_or_404(
        Membre,
        id=membre_id,
    )

    erreur = None

    if request.method == "POST":
        try:
            logger.info(
                "Suppression du membre : %s",
                membre,
            )

            membre.delete()

            return redirect(
                "bibliothecaire:liste_membres"
            )

        except ProtectedError:
            erreur = (
                "Impossible de supprimer ce membre "
                "car il possède un historique d'emprunts."
            )

    return render(
        request,
        "bibliothecaire/confirmer_suppression_membre.html",
        {
            "membre": membre,
            "erreur": erreur,
        },
    )

@user_passes_test(est_bibliothecaire)
def liste_medias(request):
    livres = Livre.objects.all().order_by("nom")
    dvds = Dvd.objects.all().order_by("nom")
    cds = Cd.objects.all().order_by("nom")
    jeux = JeuDePlateau.objects.all().order_by("nom")

    return render(
        request,
        "bibliothecaire/liste_medias.html",
        {
            "livres": livres,
            "dvds": dvds,
            "cds": cds,
            "jeux": jeux,
        },
    )

@user_passes_test(est_bibliothecaire)
def ajouter_livre(request):
    if request.method == "POST":
        form = LivreForm(request.POST)

        if form.is_valid():
            livre = form.save()

            logger.info(
                "Ajout du livre : %s",
                livre,
            )

            return redirect(
                "bibliothecaire:liste_medias"
            )

    else:
        form = LivreForm()

    return render(
        request,
        "bibliothecaire/formulaire_media.html",
        {
            "form": form,
            "titre": "Ajouter un livre",
        },
    )

@user_passes_test(est_bibliothecaire)
def ajouter_dvd(request):
    if request.method == "POST":
        form = DvdForm(request.POST)

        if form.is_valid():
            dvd = form.save()

            logger.info(
                "Ajout du DVD : %s",
                dvd,
            )

            return redirect(
                "bibliothecaire:liste_medias"
            )

    else:
        form = DvdForm()

    return render(
        request,
        "bibliothecaire/formulaire_media.html",
        {
            "form": form,
            "titre": "Ajouter un DVD",
        },
    )

@user_passes_test(est_bibliothecaire)
def ajouter_cd(request):
    if request.method == "POST":
        form = CdForm(request.POST)

        if form.is_valid():
            cd = form.save()

            logger.info(
                "Ajout du CD : %s",
                cd,
            )

            return redirect(
                "bibliothecaire:liste_medias"
            )

    else:
        form = CdForm()

    return render(
        request,
        "bibliothecaire/formulaire_media.html",
        {
            "form": form,
            "titre": "Ajouter un CD",
        },
    )

@user_passes_test(est_bibliothecaire)
def ajouter_jeu(request):
    if request.method == "POST":
        form = JeuDePlateauForm(request.POST)

        if form.is_valid():
            jeu = form.save()

            logger.info(
                "Ajout du jeu de plateau : %s",
                jeu,
            )

            return redirect(
                "bibliothecaire:liste_medias"
            )

    else:
        form = JeuDePlateauForm()

    return render(
        request,
        "bibliothecaire/formulaire_media.html",
        {
            "form": form,
            "titre": "Ajouter un jeu de plateau",
        },
    )

@user_passes_test(est_bibliothecaire)
def liste_emprunts(request):
    emprunts = Emprunt.objects.all().order_by(
        "-date_emprunt"
    )

    return render(
        request,
        "bibliothecaire/liste_emprunts.html",
        {
            "emprunts": emprunts,
        },
    )

@user_passes_test(est_bibliothecaire)
def ajouter_emprunt(request):
    erreur = None

    if request.method == "POST":
        form = EmpruntForm(request.POST)

        if form.is_valid():
            membre = form.cleaned_data["membre"]
            media = form.cleaned_data["media"]

            try:
                emprunt = creer_emprunt(
                    membre,
                    media,
                )

                logger.info(
                    "Création de l'emprunt : %s",
                    emprunt,
                )

                return redirect(
                    "bibliothecaire:liste_emprunts"
                )


            except ValidationError as exception:

                erreur = exception.message

                logger.warning(

                    "Emprunt refusé pour %s : %s",

                    membre,

                    erreur,

                )

    else:
        form = EmpruntForm()

    return render(
        request,
        "bibliothecaire/formulaire_emprunt.html",
        {
            "form": form,
            "erreur": erreur,
        },
    )

@user_passes_test(est_bibliothecaire)
def retour_emprunt(request, emprunt_id):
    emprunt = get_object_or_404(
        Emprunt,
        id=emprunt_id,
    )

    erreur = None

    if request.method == "POST":
        try:
            retourner_emprunt(emprunt)
            logger.info(
                "Retour de l'emprunt : %s",
                emprunt,
            )

            return redirect(
                "bibliothecaire:liste_emprunts"
            )

        except ValidationError as exception:
            erreur = exception.message

    return render(
        request,
        "bibliothecaire/confirmer_retour.html",
        {
            "emprunt": emprunt,
            "erreur": erreur,
        },
    )