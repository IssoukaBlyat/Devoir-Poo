from django import forms

from .models import (
    Cd,
    Dvd,
    Emprunt,
    JeuDePlateau,
    Livre,
    Media,
    Membre,
)

class MembreForm(forms.ModelForm):
    class Meta:
        model = Membre

        fields = [
            'nom',
            'prenom',
            'email',
        ]

class LivreForm(forms.ModelForm):
    class Meta:
        model = Livre

        fields = [
            "nom",
            "auteur",
        ]


class DvdForm(forms.ModelForm):
    class Meta:
        model = Dvd

        fields = [
            "nom",
            "realisateur",
        ]


class CdForm(forms.ModelForm):
    class Meta:
        model = Cd

        fields = [
            "nom",
            "artiste",
        ]


class JeuDePlateauForm(forms.ModelForm):
    class Meta:
        model = JeuDePlateau

        fields = [
            "nom",
            "createur",
        ]

class EmpruntForm(forms.Form):
    membre = forms.ModelChoiceField(
        queryset=Membre.objects.all(),
        label="Membre",
    )

    media = forms.ModelChoiceField(
        queryset=Media.objects.filter(disponible=True),
        label="Média",
    )