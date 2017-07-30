from django.db import models
from django.contrib.auth.models import User
from fsmedhrocore.models import BasicHistory


class Kunde(BasicHistory):
    """
    Extends django.contrib.auth.models.User if already registered
    """
    user = models.OneToOneField(User, blank=True, null=True)  # optional link to fsmedhro-User

    anschrift = models.CharField(max_length=255, blank=True, null=True)
    bemerkung = models.TextField(blank=True, null=True)
    tel = models.CharField(max_length=16, blank=True, null=True)

    # old information. Will be ignored if 'user' is set
    kunden_id = models.PositiveIntegerField(blank=True, null=True)
    kunden_name = models.CharField(max_length=30, blank=True, null=True)
    kunden_vorname = models.CharField(max_length=30, blank=True, null=True)
    kunden_email = models.CharField(max_length=30, blank=True, null=True)
    # geschlecht_id_f = models.ForeignKey(Tblgeschlecht)
    # studg_id_f = models.ForeignKey(Tblstudiengang)
    # kunden_timestamp = models.DateTimeField()

    def __str__(self):
        """
        returns "[Vorname] [Nachname]"
        """
        if self.user:
            return self.user.get_full_name()
        else:
            full_name = '%s %s' % (self.kunden_vorname, self.kunden_name)
            return full_name.strip()

    class Meta:
        verbose_name = "Kundin/Kunde"
        verbose_name_plural = "Kundinnen/Kunden"