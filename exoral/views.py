from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404, redirect, render
from .models import Testat, Pruefer, Frage
from fsmedhrocore.views import user_new


@login_required
def moduswahl(request):
    context = {'user': request.user}
    return render(request, 'exoral/moduswahl.html', context)


@login_required
def testatwahl(request, modus):

    try:
        studiengang = request.user.fachschaftuser.studiengang
        studienabschnitt = request.user.fachschaftuser.studienabschnitt
    except ObjectDoesNotExist:
        return redirect(user_new)  # neuen Fachschaft-User anlegen (für Studiengang etc.)

    testate = Testat.objects.filter(active=True,
                                    studienabschnitt=studienabschnitt,
                                    studiengang=studiengang)

    context = {'user': request.user, 'modus': modus, 'testate': testate}

    return render(request, 'exoral/testatwahl.html', context)


@login_required
def prueferwahl(request, modus, testat_id):
    testat = get_object_or_404(Testat, pk=testat_id)

    try:
        studiengang = request.user.fachschaftuser.studiengang
        studienabschnitt = request.user.fachschaftuser.studienabschnitt
    except ObjectDoesNotExist:
        return redirect(user_new)  # neuen Fachschaft-User anlegen (für Studiengang etc.)

    pruefer = Pruefer.objects.filter(testat=testat,
                                     active=True,
                                     studienabschnitt=studienabschnitt,
                                     studiengang=studiengang)
    context = {'user': request.user, 'modus': modus, 'testat': testat, 'pruefer': pruefer}

    return render(request, 'exoral/prueferwahl.html', context)


@login_required
def fragenliste(request, modus, testat_id, pruefer_id):
    testat = get_object_or_404(Testat, pk=testat_id)
    pruefer = get_object_or_404(Pruefer, pk=pruefer_id)
    fragen = Frage.objects.filter(pruefer=pruefer,
                                  testat=testat,
                                  sichtbar=True)
    context = {'user': request.user, 'modus': modus, 'testat': testat, 'pruefer': pruefer, 'fragen': fragen}
    return render(request, 'exoral/fragenliste.html', context)
