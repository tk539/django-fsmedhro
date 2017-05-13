from django.db import models
from django.contrib.auth.models import User


class Studienabschnitt(models.Model):
    """
    z.B. "1. Semester", "2. Semester", "Physikum", "STEX", "PJ", ...
    """
    bezeichnung = models.CharField(max_length=30)
    sortierung = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.bezeichnung

    class Meta:
        verbose_name = "Studienabschnitt/Semester"
        verbose_name_plural = "Studienabschnitte/Semester"
        ordering = ['sortierung']


class Studiengang(models.Model):
    """
    z.B. "Humanmedizin", "Zahnmedizin", ...
    """
    bezeichnung = models.CharField(max_length=30)
    studienabschnitt = models.ManyToManyField(Studienabschnitt, blank=True, related_name="studiengang")

    def __str__(self):
        return self.bezeichnung

    class Meta:
        verbose_name = "Studiengang"
        verbose_name_plural = "Studiengänge"


class Gender(models.Model):
    bezeichnung = models.CharField(max_length=30)
    endung = models.CharField(max_length=8, null=True, blank=True)  # z.B. "in" für "weiblich" -> "Studentin"

    def __str__(self):
        return self.bezeichnung

    class Meta:
        verbose_name = "Gender/Geschlecht"
        verbose_name_plural = "Gender/Geschlechter"


class FachschaftUser(models.Model):
    """
    Extends django.contrib.auth.models.User
    FachschaftUser = "StudentInnen allgemein"
    """
    user = models.OneToOneField(User)
    gender = models.ForeignKey(Gender, on_delete=models.PROTECT)  # Geschlecht
    studienabschnitt = models.ForeignKey(Studienabschnitt, on_delete=models.PROTECT)
    studiengang = models.ForeignKey(Studiengang, on_delete=models.PROTECT)
    nickname = models.CharField(max_length=30, unique=True)  # anonymer Spitzname

    def __str__(self):
        """
        returns "[Vorname] [Nachname]"
        """
        return self.user.get_full_name()

    class Meta:
        verbose_name = "StudentIn"
        verbose_name_plural = "StudentInnen"


class Fach(models.Model):
    bezeichnung = models.CharField(max_length=30)

    def __str__(self):
        return self.bezeichnung

    class Meta:
        verbose_name = "Fach"
        verbose_name_plural = "Fächer"
        ordering = ("bezeichnung",)


class Dozent(models.Model):
    titel = models.CharField(max_length=30, null=True, blank=True)
    vorname = models.CharField(max_length=30, null=True, blank=True)
    nachname = models.CharField(max_length=30)
    # studienabschnitt = models.ManyToManyField(Studienabschnitt)
    # studiengang = models.ManyToManyField(Studiengang)
    fach = models.ForeignKey(Fach, on_delete=models.CASCADE, null=True, blank=True)

    # aktiv = models.BooleanField
    # Typ? (Professor...)

    def get_full_name(self):
        """
        returns "[Titel] [Vorname] [Nachname]"
        """
        full_name = self.nachname  # "Nachname"

        if self.vorname:
            full_name = "%s %s" % (self.vorname, full_name)  # "Vorname Nachname"
        if self.titel:
            full_name = "%s %s" % (self.titel, full_name)  # "Titel Vorname Nachname"

        return full_name

    def get_full_name_nachname(self):
        """
        returns "[Nachname], [Vorname] ([Titel])"
        """
        full_name_nachname = self.nachname  # "Nachname"

        if self.vorname:
            full_name_nachname = "%s, %s" % (full_name_nachname, self.vorname)  # "Nachname, Vorname"
        if self.titel:
            full_name_nachname = "%s (%s)" % (full_name_nachname, self.titel)  # "Nachname, Vorname (Titel)"

        return full_name_nachname

    def __str__(self):
        return self.get_full_name()

    class Meta:
        verbose_name = "Dozent"
        verbose_name_plural = "Dozenten"
        ordering = ("nachname",)

class BasicHistory(models.Model):
    """
    Abstracte model-Klasse um mitzuschreiben, wann welcher User einen Eintrag hinzugefügt und wann zuletzt geändert hat.
    nicht User -> History Abfrage möglich
    """
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="+", blank=True)
    modified_date = models.DateTimeField(auto_now=True)  # Timestamp
    modified_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="+")
    version = models.PositiveIntegerField(blank=True)

    def save(self, *args, **kwargs):
        # Versionsnummer, 1. save User -> created und modified

        # if insert new, set created_by = modified_by and version = 1
        # else increase version
        if self._state.adding or self.pk is None:
            self.created_by = self.modified_by
            self.version = 1
        else:
            self.version = models.F('version') + 1

        super(BasicHistory, self).save(*args, **kwargs)  # Call the "real" save() method.

    class Meta:
        abstract = True
