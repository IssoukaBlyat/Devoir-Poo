from django.core.exceptions import ValidationError
from django.utils import timezone

from .models import Emprunt

def membre_en_retard(membre):
    return Emprunt.objects.filter(
        membre=membre,
        date_retour__isnull=True,
        date_echeance__lt=timezone.now(),
    ).exists()


def nombre_emprunts_actifs(membre):
    return Emprunt.objects.filter(
        membre=membre,
        date_retour__isnull=True,
    ).count()


def creer_emprunt(membre, media):

    if membre_en_retard(membre):
        raise ValidationError(
            "Ce membre possède un emprunt en retard."
        )

    if nombre_emprunts_actifs(membre) >= 3:
        raise ValidationError(
            "Ce membre possède déjà trois emprunts."
        )

    if not media.disponible:
        raise ValidationError(
            "Ce média n'est pas disponible."
        )

    emprunt = Emprunt.objects.create(
        membre=membre,
        media=media,
    )

    media.disponible = False
    media.save()

    return emprunt


def retourner_emprunt(emprunt):

    if emprunt.date_retour is not None:
        raise ValidationError(
            "Cet emprunt a déjà été retourné."
        )

    emprunt.date_retour = timezone.now()
    emprunt.save()

    emprunt.media.disponible = True
    emprunt.media.save()