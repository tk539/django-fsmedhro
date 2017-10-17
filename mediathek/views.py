from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from mediathek.models import Kunde, Bestellung, Sammelbestellung, Angebot, BestellungPosition
from fsmedhrocore.models import BasicHistory
from django.contrib import messages


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

    context = {'bestellung': bestellung, 'positionen': positionen}

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
