from datetime import timedelta

from django.db import models
from django.utils import timezone

class Media(models.Model):
    nom = models.CharField(max_length=200)
    disponible = models.BooleanField(default=True)

    def __str__(self):
        return self.nom

class Livre(Media):
    auteur = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.nom} - {self.auteur}'


class Dvd(Media):
    realisateur = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.nom} - {self.realisateur}'


class Cd(Media):
    artiste = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.nom} - {self.artiste}'

class JeuDePlateau(models.Model):
    nom = models.CharField(max_length=200)
    createur = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.nom} - {self.createur}'

class Membre(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    def __str__(self):
        return f'{self.prenom} - {self.nom}'

class Emprunt(models.Model):
    membre = models.ForeignKey(
        Membre,
        on_delete=models.PROTECT,
        related_name='emprunts',
    )

    media = models.ForeignKey(
        Media,
        on_delete=models.PROTECT,
        related_name='emprunts',
    )

    date_emprunt = models.DateTimeField(
        default=timezone.now,
    )

    date_echeance = models.DateTimeField(
        blank=True
    )

    date_retour = models.DateTimeField(
        null=True,
        blank=True
    )

    def save(self, *args, **kwargs):
        if not self.date_echeance:
            self.date_echeance = (
                self.date_emprunt
                + timedelta(days=7)
            )

        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.membre} - {self.media}'