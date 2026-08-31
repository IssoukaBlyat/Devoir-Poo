from datetime import timedelta

from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .forms import EmpruntForm

from .models import (
    Emprunt,
    Livre,
    Membre,
    JeuDePlateau,
)
from .services import creer_emprunt, retourner_emprunt


class BaseBibliothecaireTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="bibliothecaire",
            password="motdepasse123",
            is_staff=True,
        )

        self.client.login(
            username="bibliothecaire",
            password="motdepasse123",
        )

class MembreTests(BaseBibliothecaireTest):

    def test_creation_membre(self):
        response = self.client.post(
            reverse("bibliothecaire:creer_membre"),
            {
                "nom": "Dupont",
                "prenom": "Jean",
                "email": "jean@example.com",
            },
        )

        self.assertEqual(response.status_code, 302)

        self.assertTrue(
            Membre.objects.filter(
                email="jean@example.com"
            ).exists()
        )

    def test_liste_membres(self):
        Membre.objects.create(
            nom="Dupont",
            prenom="Jean",
            email="jean@example.com",
        )

        response = self.client.get(
            reverse("bibliothecaire:liste_membres")
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        self.assertContains(
            response,
            "Dupont",
        )

    def test_modification_membre(self):
        membre = Membre.objects.create(
            nom="Dupont",
            prenom="Jean",
            email="jean@example.com",
        )

        response = self.client.post(
            reverse(
                "bibliothecaire:modifier_membre",
                args=[membre.id],
            ),
            {
                "nom": "Durand",
                "prenom": "Jean",
                "email": "jean@example.com",
            },
        )

        self.assertEqual(
            response.status_code,
            302,
        )

        membre.refresh_from_db()

        self.assertEqual(
            membre.nom,
            "Durand",
        )

    def test_suppression_membre(self):
        membre = Membre.objects.create(
            nom="Dupont",
            prenom="Jean",
            email="jean@example.com",
        )

        response = self.client.post(
            reverse(
                "bibliothecaire:supprimer_membre",
                args=[membre.id],
            )
        )

        self.assertEqual(
            response.status_code,
            302,
        )

        self.assertFalse(
            Membre.objects.filter(
                id=membre.id
            ).exists()
        )


class MediaTests(BaseBibliothecaireTest):

    def test_ajout_livre(self):
        response = self.client.post(
            reverse("bibliothecaire:ajouter_livre"),
            {
                "nom": "Dune",
                "auteur": "Frank Herbert",
            },
        )

        self.assertEqual(
            response.status_code,
            302,
        )

        self.assertTrue(
            Livre.objects.filter(
                nom="Dune"
            ).exists()
        )

    def test_liste_medias(self):
        Livre.objects.create(
            nom="Dune",
            auteur="Frank Herbert",
        )

        response = self.client.get(
            reverse("bibliothecaire:liste_medias")
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        self.assertContains(
            response,
            "Dune",
        )

class EmpruntTests(BaseBibliothecaireTest):

    def setUp(self):
        super().setUp()

        self.membre = Membre.objects.create(
            nom="Dupont",
            prenom="Jean",
            email="jean@example.com",
        )

        self.livre = Livre.objects.create(
            nom="Dune",
            auteur="Frank Herbert",
        )

    def test_creation_emprunt(self):
        emprunt = creer_emprunt(
            self.membre,
            self.livre,
        )

        self.assertIsNotNone(
            emprunt.id
        )

        self.livre.refresh_from_db()

        self.assertFalse(
            self.livre.disponible
        )

    def test_retour_emprunt(self):
        emprunt = creer_emprunt(
            self.membre,
            self.livre,
        )

        retourner_emprunt(
            emprunt
        )

        emprunt.refresh_from_db()
        self.livre.refresh_from_db()

        self.assertIsNotNone(
            emprunt.date_retour
        )

        self.assertTrue(
            self.livre.disponible
        )

    def test_echeance_sept_jours(self):
        emprunt = creer_emprunt(
            self.membre,
            self.livre,
        )

        difference = (
                emprunt.date_echeance
                - emprunt.date_emprunt
        )

        self.assertEqual(
            difference,
            timedelta(days=7),
        )

    def test_maximum_trois_emprunts(self):
        livre1 = Livre.objects.create(
            nom="Livre 1",
            auteur="Auteur",
        )

        livre2 = Livre.objects.create(
            nom="Livre 2",
            auteur="Auteur",
        )

        livre3 = Livre.objects.create(
            nom="Livre 3",
            auteur="Auteur",
        )

        livre4 = Livre.objects.create(
            nom="Livre 4",
            auteur="Auteur",
        )

        creer_emprunt(
            self.membre,
            livre1,
        )

        creer_emprunt(
            self.membre,
            livre2,
        )

        creer_emprunt(
            self.membre,
            livre3,
        )

        with self.assertRaises(ValidationError):
            creer_emprunt(
                self.membre,
                livre4,
            )

    def test_membre_en_retard_bloque(self):
        premier_livre = Livre.objects.create(
            nom="Ancien livre",
            auteur="Auteur",
        )

        emprunt = creer_emprunt(
            self.membre,
            premier_livre,
        )

        emprunt.date_echeance = (
                timezone.now()
                - timedelta(days=1)
        )

        emprunt.save()

        nouveau_livre = Livre.objects.create(
            nom="Nouveau livre",
            auteur="Auteur",
        )

        with self.assertRaises(ValidationError):
            creer_emprunt(
                self.membre,
                nouveau_livre,
            )

    def test_jeu_de_plateau_non_empruntable(self):
        jeu = JeuDePlateau.objects.create(
            nom="Catan",
            createur="Klaus Teuber",
        )

        form = EmpruntForm()

        medias = form.fields[
            "media"
        ].queryset

        self.assertFalse(
            medias.filter(
                nom=jeu.nom
            ).exists()
        )

class SecuriteTests(TestCase):

    def test_acces_sans_connexion(self):
        response = self.client.get(
            reverse(
                "bibliothecaire:tableau_bord"
            )
        )

        self.assertNotEqual(
            response.status_code,
            200,
        )