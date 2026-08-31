from django.shortcuts import render

from bibliothecaire.models import (
    JeuDePlateau,
    Media,
)


def liste_medias(request):
    medias = Media.objects.all()
    jeux = JeuDePlateau.objects.all()

    return render(
        request,
        'membre/liste_medias.html',
        {
            "medias": medias,
            "jeux": jeux,
        },
    )