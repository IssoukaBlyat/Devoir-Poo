from django.test import TestCase
from django.urls import reverse

from bibliothecaire.models import (
    JeuDePlateau,
    Livre,
)


class CataloguePublicTests(TestCase):

    def test_affichage_medias(self):
        Livre.objects.create(
            nom="Dune",
            auteur="Frank Herbert",
        )

        JeuDePlateau.objects.create(
            nom="Catan",
            createur="Klaus Teuber",
        )

        response = self.client.get(
            reverse("membre:liste_medias")
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        self.assertContains(
            response,
            "Dune",
        )

        self.assertContains(
            response,
            "Catan",
        )