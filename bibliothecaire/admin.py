from django.contrib import admin

from .models import (
    Cd,
    Dvd,
    Emprunt,
    JeuDePlateau,
    Livre,
    Media,
    Membre,
)


admin.site.register(Media)
admin.site.register(Livre)
admin.site.register(Dvd)
admin.site.register(Cd)
admin.site.register(JeuDePlateau)
admin.site.register(Membre)
admin.site.register(Emprunt)