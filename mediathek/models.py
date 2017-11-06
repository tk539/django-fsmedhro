from django.db import models
from django.contrib.auth.models import User
from fsmedhrocore.models import BasicHistory
from django.utils import timezone
import decimal


class Kunde(models.Model):
    """
    Extends django.contrib.auth.models.User
    """
    user = models.OneToOneField(User)

    anschrift = models.TextField(blank=True, null=True)
    tel = models.CharField(max_length=16, blank=True, null=True)
    bemerkung = models.TextField(blank=True, null=True)

    def get_user_first_name(self):
        return self.user.first_name
    get_user_first_name.short_description = "Vorname"
    get_user_first_name.admin_order_field = 'user__first_name'

    def get_user_last_name(self):
        return self.user.last_name
    get_user_last_name.short_description = "Nachname"
    get_user_last_name.admin_order_field = 'user__last_name'

    def __str__(self):
        """
        returns "[Vorname] [Nachname]"
        """
        return self.user.get_full_name()

    class Meta:
        verbose_name = "Kundin/Kunde"
        verbose_name_plural = "Kundinnen/Kunden"
        ordering = ("user__last_name",)


class Sammelbestellung(models.Model):
    bezeichnung = models.CharField(max_length=30)
    start = models.DateTimeField()
    ende = models.DateTimeField()
    abgeschlossen = models.BooleanField(default=False, verbose_name="abgeschlossen")

    def __str__(self):
        return self.bezeichnung

    class Meta:
        verbose_name = "Sammelbestellung"
        verbose_name_plural = "Sammelbestellungen"
        ordering = ("abgeschlossen", "-ende")


class Ware(models.Model):
    bezeichnung = models.CharField(max_length=40)
    marke = models.CharField(max_length=30, null=True, blank=True)
    variation = models.CharField(max_length=30, null=True, blank=True)

    def __str__(self):
        s = self.bezeichnung
        if self.marke:
            s = "{}: {}".format(self.marke, s)
        if self.variation:
            s = "{} ({})".format(s, self.variation)
        return s  # "marke: bezeichnung (variation)"

    class Meta:
        verbose_name = "Ware"
        verbose_name_plural = "Waren"
        ordering = ("marke", "bezeichnung", "variation")


class Angebot(models.Model):
    preis = models.DecimalField(max_digits=8, decimal_places=2)  # max. 999999.99
    ware = models.ForeignKey(Ware, on_delete=models.CASCADE)
    sammelbestellung = models.ForeignKey(Sammelbestellung, on_delete=models.CASCADE)

    def get_preis_str(self):
        return "{} €".format(self.preis).replace(".", ",")

    def get_best_count(self):
        count = 0
        for pos in self.bestellungposition_set.all():
            count += pos.anzahl
        return count

    def get_best_total_sale(self):
        return decimal.Decimal(self.get_best_count()) * self.preis

    def __str__(self):
        return "{} - {} - {}".format(self.sammelbestellung, self.ware, self.get_preis_str())

    class Meta:
        verbose_name = "Angebot"
        verbose_name_plural = "Angebote"
        ordering = ("ware__marke", "ware__bezeichnung", "ware__variation")


class Auftrag(models.Model):

    ERSTELLT, BEARBEITET, ABGESCHLOSSEN = range(0, 3)

    STATUS = (
        (ERSTELLT, 'erstellt'),
        (BEARBEITET, 'bearbeitet'),
        (ABGESCHLOSSEN, 'abgeschlossen'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    datum = models.DateField(default=timezone.datetime.today, verbose_name="Auftrags-Datum")
    status = models.IntegerField(choices=STATUS, default=ERSTELLT)

    # override Model API method, STATUS can be overridden in subclasses
    def get_status_display(self):
        return self.STATUS[self.status][1]
    get_status_display.short_description = 'Status'
    get_status_display.admin_order_field = 'status'

    def get_user_first_name(self):
        return self.user.first_name
    get_user_first_name.short_description = "Vorname"
    get_user_first_name.admin_order_field = 'user__first_name'

    def get_user_last_name(self):
        return self.user.last_name
    get_user_last_name.short_description = "Nachname"
    get_user_last_name.admin_order_field = 'user__last_name'

    def get_auf_id(self):
        return self.pk
    get_auf_id.short_description = "Auftr.-Nr."

    def __str__(self):
        return "{} {} ({}), {}".format(
            self._meta.verbose_name_raw, self.pk, self.datum, self.get_status_display())

    class Meta:
        verbose_name = "Auftrag"
        verbose_name_plural = "Aufträge"
        ordering = ('-datum', 'status',)


class Bestellung(Auftrag):

    Auftrag.STATUS = (
        (Auftrag.ERSTELLT, 'bestellt'),
        (Auftrag.BEARBEITET, 'abholbereit'),
        (Auftrag.ABGESCHLOSSEN, 'abgeschlossen'),
    )

    bezahlt = models.BooleanField(default=False, verbose_name="bezahlt")
    # has BestellungPosition

    def get_status_display(self):
        return self.STATUS[self.status][1]
    get_status_display.short_description = 'Status'
    get_status_display.admin_order_field = 'status'

    def get_bezahlbetrag(self):
        summe = decimal.Decimal('0.00')
        for pos in self.bestellungposition_set.all():
            summe += pos.angebot.preis * pos.anzahl
        return "{} €".format(summe).replace(".", ",")
    get_bezahlbetrag.short_description = 'zu zahlen'

    class Meta:
        verbose_name = "Sammelbestellung(Auftrag)"
        verbose_name_plural = "Sammelbestellungen(Aufträge)"


class BestellungPosition(models.Model):
    bestellung = models.ForeignKey(Bestellung, on_delete=models.CASCADE)
    angebot = models.ForeignKey(Angebot, on_delete=models.PROTECT)
    anzahl = models.PositiveSmallIntegerField(default=1)

    def __str__(self):
        return "{}x {}".format(self.anzahl, self.angebot.ware)

    class Meta:
        verbose_name = "Bestellungs-Position"
        verbose_name_plural = "Bestellungs-Positionen"
        ordering = ("angebot__ware__marke", "angebot__ware__bezeichnung", "angebot__ware__variation")


class Einstellungen(models.Model):
    timestamp = models.DateTimeField(auto_now=True)
    oeffnungszeiten = models.TextField(null=True, blank=True, verbose_name="Öffnungszeiten")
    konto_inhaber = models.CharField(max_length=30, default='KontoinhaberIn', verbose_name="KontoinhaberIn")
    konto_iban = models.CharField(max_length=22, default='DE00000000000000000000', verbose_name="Konto IBAN")

    def __str__(self):
        return "Einstellungen (Stand: {:%d.%m.%y %H:%M})".format(self.timestamp)

    class Meta:
        verbose_name = "Einstellungen"
        verbose_name_plural = "Einstellungen"
