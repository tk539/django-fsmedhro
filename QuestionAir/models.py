from django.db import models
from django.contrib.auth.models import User
from fsmedhrocore.models import Dozent, BasicHistory, Studienabschnitt, Studiengang
from django.utils import timezone


#TODO: bitte Dokument überprüfen


class QuestionAirUser(models.Model):
    """
    Extends django.contrib.auth.models.User
    """
    user = models.OneToOneField(User)

    def __str__(self):
        # Vorname + Nachname
        return self.user.get_full_name()

class Fach(models.Model):
    name = models.CharField(max_length=500)
    Studienabschnitt = models.ManyToManyField(Studienabschnitt)
    Studiengang=models.ManyToManyField(Studiengang)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Fach"
        verbose_name_plural = "Fächer"

class Klausur(models.Model):
    name=models.CharField(max_length=120)
    Fach=models.ManyToManyField(Fach)
    datum=models.DateField(default=timezone.datetime.today, verbose_name="Klausurdatum")

    class Meta:
        verbose_name= "Klausur"
        verbose_name_plural= "Klausuren"

    def __str__(self):
        return self.name

class Frage(models.Model):
        #TODO: change relationship to ManytoOne
    Klausur = models.ManyToManyField(Klausur)

        #TODO: bearbeitbare Texte erstellen
    Fragentext = models.TextField
    option1 = models.CharField
    option2 = models.CharField
    option3 = models.CharField
    option4 = models.CharField
    option5 = models.CharField
    answerA = models.TextField
    answerB = models.TextField
    answerC = models.TextField
    answerD = models.TextField
    answerE = models.TextField
    submitter = models.ManyToManyField(QuestionAirUser)
    correctAnswer = models.PositiveIntegerField(default=1)

    #TODO: correctAnswer als aufwahlfeld von answerA-E
    #TODO: option1-5 als optional Field --> nur angezeigt wenn Inhalt vorhanden

    class Meta:
        verbose_name="Frage"
        verbose_name_plural="Fragen"

class Kommentar(BasicHistory):
    text=models.TextField()
    visible=models.BooleanField(default=False)
    frage=models.ForeignKey(Frage)

    def __str__(self):
        return self.text

    class Meta:
        verbose_name="Kommentar"
        verbose_name_plural="Kommentare"