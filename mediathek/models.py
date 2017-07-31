from django.db import models
from django.contrib.auth.models import User
from fsmedhrocore.models import BasicHistory


class Kunde(BasicHistory):
    """
    Extends django.contrib.auth.models.User
    """
    user = models.OneToOneField(User)

    anschrift = models.CharField(max_length=255, blank=True, null=True)
    tel = models.CharField(max_length=16, blank=True, null=True)
    bemerkung = models.TextField(blank=True, null=True)

    def __str__(self):
        """
        returns "[Vorname] [Nachname]"
        """
        return self.user.get_full_name()

    class Meta:
        verbose_name = "Kundin/Kunde"
        verbose_name_plural = "Kundinnen/Kunden"