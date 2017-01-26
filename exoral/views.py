from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404, redirect, render
from .models import Testat, Pruefer, Frage, Kommentar
from fsmedhrocore.views import user_edit
from django.contrib import messages


@login_required
def moduswahl(request):
    return render(request, 'exoral/moduswahl.html')


@login_required
def testatwahl(request, modus):

    try:
        studiengang = request.user.fachschaftuser.studiengang
        studienabschnitt = request.user.fachschaftuser.studienabschnitt
    except ObjectDoesNotExist:
        return redirect(user_edit)  # neuen Fachschaft-User anlegen (für Studiengang etc.)

    testate = Testat.objects.filter(active=True,
                                    studienabschnitt=studienabschnitt,
                                    studiengang=studiengang).order_by('bezeichnung')

    if not testate.exists():
        messages.add_message(request, messages.INFO, 'keine Testate abrufbar...')

    context = {'modus': modus, 'testate': testate}

    return render(request, 'exoral/testatwahl.html', context)


@login_required
def prueferwahl(request, modus, testat_id):
    testat = get_object_or_404(Testat, pk=testat_id)

    try:
        studiengang = request.user.fachschaftuser.studiengang
        studienabschnitt = request.user.fachschaftuser.studienabschnitt
    except ObjectDoesNotExist:
        return redirect(user_edit)  # neuen Fachschaft-User anlegen (für Studiengang etc.)

    pruefer = Pruefer.objects.filter(testat=testat,
                                     active=True,
                                     studienabschnitt=studienabschnitt,
                                     studiengang=studiengang).order_by('nachname', 'vorname')
    if not pruefer.exists():
        messages.add_message(request, messages.INFO, 'keine Prüfer abrufbar...')

    context = {'modus': modus, 'testat': testat, 'pruefer_list': pruefer}

    return render(request, 'exoral/prueferwahl.html', context)


@login_required
def fragenliste(request, modus, testat_id, pruefer_id):
    testat = get_object_or_404(Testat, pk=testat_id)
    pruefer = get_object_or_404(Pruefer, pk=pruefer_id)
    fragen = Frage.objects.filter(pruefer=pruefer,
                                  testat=testat,
                                  sichtbar=True).order_by('-score', '-datum')
    kommentare = Kommentar.objects.filter(pruefer=pruefer,
                                          sichtbar=True).order_by('-created_date')

    if not fragen.exists():
        messages.add_message(request, messages.INFO, 'keine Fragen abrufbar...')

    if not kommentare.exists():
        messages.add_message(request, messages.INFO, 'keine Prüfer-Kommentare abrufbar...')

    context = {'modus': modus, 'testat': testat, 'pruefer': pruefer,
               'fragen': fragen, 'kommentare': kommentare}

    return render(request, 'exoral/fragenliste.html', context)
