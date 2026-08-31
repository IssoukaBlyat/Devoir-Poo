# Rapport

## 1. Présentation du projet

Le devoir consiste à développer une application web permettant de gérer une médiathèque.

L'application a été développée avec Django et comporte deux parties principales :

- un espace public destiné à la consultation des médias ;
- un espace réservé aux bibliothécaires destiné à la gestion de la médiathèque.

## 2. Architecture du projet

Le projet Django comporte deux applications :

### bibliothecaire

Cette application gère :

- les membres ;
- les livres ;
- les DVD ;
- les CD ;
- les jeux de plateau ;
- les emprunts ;
- les retours.

### membre

Cette application permet de consulter publiquement le catalogue de la médiathèque.

## 3. Modèle de données

Une classe parent `Media` est utilisée pour représenter les médias empruntables.

Les classes suivantes héritent de `Media` :

- `Livre`
- `Dvd`
- `Cd`

La classe `JeuDePlateau` est séparée car les jeux de plateau ne peuvent pas être empruntés.

La classe `Membre` représente un utilisateur inscrit à la médiathèque.

La classe `Emprunt` associe un membre et un média.

## 4. Gestion des emprunts

Plusieurs règles métier ont été mises en place.

Un membre ne peut pas avoir plus de trois emprunts simultanément.

Un membre possédant un emprunt en retard ne peut pas effectuer de nouvel emprunt.

Lorsqu'un média est emprunté, son attribut `disponible` passe à `False`.

Lors du retour, l'attribut revient à `True`.

La date d'échéance est automatiquement calculée sept jours après la date d'emprunt.

## 5. Jeux de plateau

Les jeux de plateau ne peuvent pas être empruntés.

Ils sont donc volontairement séparés de la classe `Media`.

Ils apparaissent dans le catalogue mais ne peuvent pas être sélectionnés lors de la création d'un emprunt.

## 6. Sécurité

L'espace bibliothécaire est protégé par le système d'authentification de Django.

Seuls les utilisateurs authentifiés disposant du statut `staff` peuvent accéder à cette partie.

Les visiteurs non authentifiés peuvent uniquement consulter le catalogue public.

## 7. Logs

Le module `logging` de Python est utilisé.

Les principales actions sont enregistrées, par exemple :

- création d'un membre ;
- modification d'un membre ;
- suppression d'un membre ;
- ajout d'un média ;
- création d'un emprunt ;
- retour d'un emprunt.

Les logs sont enregistrés dans le terminal ainsi que dans le fichier `mediatheque.log`.

## 8. Tests

Des tests automatiques Django ont été réalisés.

Les tests couvrent notamment :

- la gestion des membres ;
- la gestion des médias ;
- la création des emprunts ;
- les retours ;
- la limite de trois emprunts ;
- le blocage des membres ayant un retard ;
- la durée des emprunts ;
- la sécurité de l'espace bibliothécaire ;
- l'affichage du catalogue public.

Ils peuvent être exécutés avec :

```bash
python manage.py test