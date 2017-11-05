from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import ObjectDoesNotExist
from mediathek.models import Kunde, Bestellung, Sammelbestellung, Angebot, BestellungPosition, Einstellungen
from fsmedhrocore.models import BasicHistory
from django.contrib import messages
from django.utils import timezone
import decimal
from django.contrib.auth.models import User
import csv
from django.http import HttpResponse


def check_mediathek_mitarbeiter(user):
    return user.groups.filter(name='mediathek').exists()


def check_created_by(user, auftrag):
    if isinstance(auftrag, BasicHistory):
        return auftrag.created_by == user
    else:
        # no BosicHistory-object passed
        return None


@login_required
def index(request):

    user = request.user

    # Kundendaten abfragen. Wenn noch kein Kundenprofil, dann neu anlegen
    try:
        kunde = user.kunde
    except ObjectDoesNotExist:
        kunde = Kunde(user=user)
        kunde.save()

    bestellungen = Bestellung.objects.filter(user=user).order_by('-datum')
    aktuelle_sammelbest = Sammelbestellung.objects.filter(abgeschlossen=False).order_by('-ende')

    context = {'kunde': kunde, 'aktuelle_sammelbest': aktuelle_sammelbest, 'bestellungen': bestellungen}

    return render(request, 'mediathek/index.html', context)


@login_required
def sammelbest_auftrag_detail(request, auftrag_id):
    """
    Eine Bestellung ansehen
    :param request:
    :param auftrag_id:
    :return:
    """
    bestellung = get_object_or_404(Bestellung, pk=auftrag_id)

    if check_created_by(user=request.user, auftrag=bestellung):
        # nur der Eigentümer darf Bestellung  einsehen
        messages.add_message(request, messages.INFO, 'Diese Bestellung ist nicht von dir.')
        return redirect('mediathek:index')

    positionen = BestellungPosition.objects.filter(bestellung=bestellung)

    context = {'bestellung': bestellung,
               'positionen': positionen,
               'sammelbestellung': positionen.first().angebot.sammelbestellung,
               'einstellungen': Einstellungen.objects.last(),
               'user': request.user,
               }

    return render(request, 'mediathek/sammelbest_auftrag_detail.html', context)


@login_required
def sammelbest_auftrag_neu(request, sammelbest_id):
    """
    Eine Bestellung aufgeben
    :param request:
    :param sammelbest_id:
    :return:
    """
    sammelbestellung = get_object_or_404(Sammelbestellung, pk=sammelbest_id)

    # Sammelbestellung abgelaufen?
    if sammelbestellung.start > timezone.now() or sammelbestellung.ende < timezone.now():
        tz = timezone.get_current_timezone()
        messages.add_message(request, messages.INFO,
                             'Bestellung nur zwischen {:%d.%m.%y %H:%M} und {:%d.%m.%y %H:%M} ({}) möglich.'.format(
                                 sammelbestellung.start.astimezone(tz), sammelbestellung.ende.astimezone(tz), tz))
        return redirect('mediathek:index')

    valid_order = False
    positionen = []

    if request.method == 'POST':
        for key, value in request.POST.items():
            if key.isdigit() and value.isdigit():
                if int(value) > 0:
                    valid_order = True
                    angebot = get_object_or_404(Angebot, pk=int(key))
                    anzahl = int(value)
                    positionen.append({'angebot': angebot, 'anzahl': anzahl})
        if valid_order:
            bestellung = Bestellung(user=request.user)
            bestellung.save()
            for pos in positionen:
                position = BestellungPosition(bestellung=bestellung, angebot=pos['angebot'], anzahl=pos['anzahl'])
                position.save()
            return redirect('mediathek:sammelbest_auftrag_detail', auftrag_id=bestellung.pk)
        else:
            messages.add_message(request, messages.INFO, 'Ungültige Bestellung')
            return redirect('mediathek:index')

    angebote = Angebot.objects.filter(sammelbestellung=sammelbestellung)
    context = {'sammelbestellung': sammelbestellung, 'angebote': angebote}

    return render(request, 'mediathek/sammelbest_auftrag_neu.html', context)


@login_required
@user_passes_test(check_mediathek_mitarbeiter)
def sammelbest_zusammenfassung(request, sammelbest_id):
    sammelbestellung = get_object_or_404(Sammelbestellung, pk=sammelbest_id)

    angebote = Angebot.objects.filter(sammelbestellung=sammelbestellung)

    positionen = BestellungPosition.objects.filter(angebot__sammelbestellung=sammelbestellung)

    bestellungen = Bestellung.objects.filter(bestellungposition__in=positionen)

    kunden = User.objects.filter(auftrag__in=bestellungen).distinct().order_by('last_name', 'first_name')

    #table = [['x']*(angebote.count()+1) for i in range(len(kunden))]

    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Sammelbestellung_Zusammenfassung.csv"'

    writer = csv.writer(response, dialect=csv.excel)

    writer.writerow(["Sammelbestellung", sammelbestellung.bezeichnung,
                     "{:%d.%m.%y %H:%M}".format(sammelbestellung.start),
                     "bis",
                     "{:%d.%m.%y %H:%M}".format(sammelbestellung.ende),
                     ])

    headrow = ["Kunde"]
    for a in angebote:
        headrow.append(a.ware)

    writer.writerow(headrow)

    for i, k in enumerate(kunden):
        row = ['{}, {}'.format(k.last_name, k.first_name)]
        for j, a in enumerate(angebote):
            pos = BestellungPosition.objects.filter(
                angebot__sammelbestellung=sammelbestellung,
                angebot=a,
                bestellung__user=k
            )

            anz = 0
            for p in pos:
                anz += p.anzahl

            row.append(anz)
        writer.writerow(row)

    lastrow = ["gesamt:"]
    for a in angebote:
        lastrow.append(a.get_best_count())

    writer.writerow(lastrow)

    return response