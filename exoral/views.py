from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404, redirect, render
from .models import Testat, Pruefer, Frage, Kommentar
from fsmedhrocore.views import user_edit
from django.contrib import messages
from .forms import FrageForm, KommentarForm
from django.http import HttpResponseRedirect
from django.urls import reverse


@login_required
def moduswahl(request):
    # hier kommt die Moduswahl
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
        messages.add_message(request, messages.INFO, 'Es sind leider keine Testate abrufbar für deinen Studienabschnitt')

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
        messages.add_message(request, messages.INFO, 'Für dieses Testat ist kein Prüfer abrufbar')

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
        messages.add_message(request, messages.INFO,
                             'Für dieses Testat existieren leider noch keine Fragen. '
                             'Wenn du eine mündliche Testatfrage hast, trage sie bitte ein')

    if not kommentare.exists():
        messages.add_message(request, messages.INFO, 'Für diesen Prüfer existieren noch keine Kommentare')

    context = {'modus': modus, 'testat': testat, 'pruefer': pruefer,
               'fragen': fragen, 'kommentare': kommentare}

    return render(request, 'exoral/fragenliste.html', context)


@login_required
def frage_neu(request, modus, testat_id, pruefer_id):
    testat = get_object_or_404(Testat, pk=testat_id)
    pruefer = get_object_or_404(Pruefer, pk=pruefer_id)

    if request.method == 'POST':
        f_form = FrageForm(data=request.POST)
        if f_form.is_valid():
            frage = f_form.save(commit=False)
            frage.modified_by = request.user
            frage.save()
            messages.add_message(request, messages.SUCCESS, 'Vielen Dank, dass du deine Frage eingetragen hast')
            # return redirect(fragenliste, modus=modus, testat_id=frage.testat.pk, pruefer_id=frage.pruefer.pk)
            return HttpResponseRedirect(reverse('exoral:fragenliste', args=(modus, testat.pk, pruefer.pk)))

    else:
        f_form = FrageForm(initial={'testat': testat, 'pruefer': pruefer})

    context = {
        'f_form': f_form,
        'modus': modus, 'testat': testat, 'pruefer': pruefer,
    }

    return render(request, 'exoral/frage_neu.html', context)


def frage_score(request, frage_id):
    testat = get_object_or_404(Testat, pk=request.POST['testat_id'])
    pruefer = get_object_or_404(Pruefer, pk=request.POST['pruefer_id'])
    frage = get_object_or_404(Frage, pk=frage_id)

    try:
        has_scored = request.session['has_scored']
    except KeyError:
        has_scored = []

    if frage.pk in has_scored:
        messages.add_message(request, messages.WARNING, 'Frage wurde bereits gescored')
    elif len(has_scored) > 10:
        messages.add_message(request, messages.WARNING, 'Nicht mehr als 10 Scores möglich')
    else:
        has_scored.append(frage.pk)
        request.session['has_scored'] = has_scored
        frage.score_up(request.user)

    messages.add_message(request, messages.SUCCESS,
                         'Du hast erfolgreich den Score der Frage erhöht. Danke, '
                         'dass du dafür keine neue Frage hinzugefügt hast.')

    return HttpResponseRedirect(reverse('exoral:fragenliste', args=('p', testat.pk, pruefer.pk)))


@login_required()
def kommentar_neu(request, modus, testat_id, pruefer_id):
    testat = get_object_or_404(Testat, pk=testat_id)
    pruefer = get_object_or_404(Pruefer, pk=pruefer_id)

    if request.method == 'POST':
        k_form = KommentarForm(data=request.POST)
        if k_form.is_valid():
            kommentar = k_form.save(commit=False)
            kommentar.modified_by = request.user
            kommentar.save()
            messages.add_message(request, messages.SUCCESS,
                                 'Wir haben deinen Kommentar erfolgreich in unsere Datenbank aufgenommen')
            # return redirect(fragenliste, modus=modus, testat_id=frage.testat.pk, pruefer_id=frage.pruefer.pk)
            return HttpResponseRedirect(reverse('exoral:fragenliste', args=(modus, testat.pk, pruefer.pk)))

    else:
        k_form = KommentarForm(initial={'pruefer': pruefer})

    context = {
        'k_form': k_form,
        'modus': modus, 'pruefer': pruefer, 'testat': testat,
    }

    return render(request, 'exoral/kommentar_neu.html', context)
