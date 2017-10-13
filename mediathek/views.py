from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import ObjectDoesNotExist
from mediathek.models import Kunde


def check_mediathek_mitarbeiter(user):
    return user.groups.filter(name='mediathek').exists()


@login_required
def mediathek_index(request):

    user = request.user

    # Kundendaten abfragen. Wenn noch kein Kundenprofil, dann neu anlegen
    try:
        kunde = user.kunde
    except ObjectDoesNotExist:
        kunde = Kunde(user=user, modified_by=user)
        kunde.save()

    context = {'kunde': kunde,}

    return render(request, 'mediathek/index.html', context)


@login_required
@user_passes_test(check_mediathek_mitarbeiter, login_url='mediathek:mediathek_index', redirect_field_name=None)
def mediathek_verwaltung(request):
    return render(request, 'mediathek/verwaltung.html')


@login_required
@user_passes_test(check_mediathek_mitarbeiter, login_url='mediathek:mediathek_index', redirect_field_name=None)
def ausleihe(request):
    return render(request, 'mediathek/ausleihe.html')