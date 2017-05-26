from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404, redirect, render
from .models import Testat, Pruefer, Frage, Kommentar, Protokoll
from fsmedhrocore.views import user_edit
from django.contrib import messages
from .forms import FrageForm, KommentarForm, ProtokollForm
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
        messages.add_message(request, messages.INFO, 'Für dein Semester sind keine Testate abrufbar')

    context = {'modus': modus, 'testate': testate}

    return render(request, 'exoral/testatwahl.html', context)


@login_required
def prueferwahl(request, modus, testat_id):
    testat = get_object_or_404(Testat, pk=testat_id)

    faecher = testat.fach.all()

    if faecher.count() == 0:
        messages.add_message(request, messages.INFO, 'Für dieses testat ist kein Fach eingetragen. ')

    pruefer = Pruefer.objects.filter(fach__in=faecher,
                                     active=True,).order_by('fach__bezeichnung', 'nachname', 'vorname')
    if not pruefer.exists():
        messages.add_message(request, messages.INFO, 'Für dieses Testat sind keine Prüfer abrufbar. ')

    pruefer_list = {}
    fach_temp = None
    for pruef in pruefer:

        if pruef.fach != fach_temp:
            pruefer_list[pruef.fach.bezeichnung] = []

        pruefer_list[pruef.fach.bezeichnung].append(
            {'pruefer': pruef, 'count': Frage.objects.filter(testat=testat, pruefer=pruef).count()})

        fach_temp = pruef.fach

    context = {'modus': modus, 'testat': testat, 'pruefer_list': pruefer_list}

    return render(request, 'exoral/prueferwahl.html', context)


@login_required
def fragenliste(request, modus, testat_id, pruefer_id):
    testat = get_object_or_404(Testat, pk=testat_id)
    pruefer = get_object_or_404(Pruefer, pk=pruefer_id)
    fragen = Frage.objects.filter(pruefer=pruefer,
                                  testat=testat,
                                  sichtbar=True).order_by('-score', '-datum')

    if not fragen.exists():
        messages.add_message(request, messages.INFO,
                             'Für dieses Testat existieren leider noch keine Fragen. '
                             'Wenn du eine mündliche Testatfrage hast, trage sie bitte ein')

    c_fragen = fragen.count()
    c_protokolle = Protokoll.objects.filter(testat=testat, pruefer=pruefer).count()
    c_kommentare = Kommentar.objects.filter(pruefer=pruefer).count()

    context = {'modus': modus, 'testat': testat, 'pruefer': pruefer, 'fragen': fragen,
               'count_fragen': c_fragen, 'count_protokolle': c_protokolle, 'count_kommentare': c_kommentare,}

    return render(request, 'exoral/fragenliste.html', context)


@login_required
def kommentarliste(request, modus, testat_id, pruefer_id):
    testat = get_object_or_404(Testat, pk=testat_id)
    pruefer = get_object_or_404(Pruefer, pk=pruefer_id)
    kommentare = Kommentar.objects.filter(pruefer=pruefer,
                                          sichtbar=True)

    if not kommentare.exists():
        messages.add_message(request, messages.INFO, 'Für diesen Prüfer existieren noch keine Kommentare')

    c_fragen = Frage.objects.filter(testat=testat, pruefer=pruefer).count()
    c_protokolle = Protokoll.objects.filter(testat=testat, pruefer=pruefer).count()
    c_kommentare = kommentare.count()

    context = {'modus': modus, 'testat': testat, 'pruefer': pruefer, 'kommentare': kommentare,
               'count_fragen': c_fragen, 'count_protokolle': c_protokolle, 'count_kommentare': c_kommentare, }

    return render(request, 'exoral/kommentarliste.html', context)



@login_required
def protokollliste(request, modus, testat_id, pruefer_id):
    testat = get_object_or_404(Testat, pk=testat_id)
    pruefer = get_object_or_404(Pruefer, pk=pruefer_id)
    protokolle = Protokoll.objects.filter(pruefer=pruefer,
                                  testat=testat,
                                  sichtbar=True).order_by('-datum')

    if not protokolle.exists():
        messages.add_message(request, messages.INFO,
                             'Für dieses Testat existieren leider noch keine Protokolle. ')

    c_fragen = Frage.objects.filter(testat=testat, pruefer=pruefer).count()
    c_protokolle = protokolle.count()
    c_kommentare = Kommentar.objects.filter(pruefer=pruefer).count()

    context = {'modus': modus, 'testat': testat, 'pruefer': pruefer, 'protokolle': protokolle,
               'count_fragen': c_fragen, 'count_protokolle': c_protokolle, 'count_kommentare': c_kommentare, }

    return render(request, 'exoral/protokollliste.html', context)


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


@login_required
def protokoll_neu(request, modus, testat_id, pruefer_id):
    testat = get_object_or_404(Testat, pk=testat_id)
    pruefer = get_object_or_404(Pruefer, pk=pruefer_id)

    if request.method == 'POST':
        p_form = ProtokollForm(data=request.POST)
        if p_form.is_valid():
            protokoll = p_form.save(commit=False)
            protokoll.modified_by = request.user
            protokoll.save()
            messages.add_message(request, messages.SUCCESS, 'Vielen Dank, dass du dein Protokoll eingetragen hast')
            # return redirect(fragenliste, modus=modus, testat_id=frage.testat.pk, pruefer_id=frage.pruefer.pk)
            return HttpResponseRedirect(reverse('exoral:protokollliste', args=(modus, testat.pk, pruefer.pk)))

    else:
        p_form = ProtokollForm(initial={'testat': testat, 'pruefer': pruefer})

    context = {
        'p_form': p_form,
        'modus': modus, 'testat': testat, 'pruefer': pruefer,
    }

    return render(request, 'exoral/protokoll_neu.html', context)


def frage_score(request, frage_id):
    testat = get_object_or_404(Testat, pk=request.POST['testat_id'])
    pruefer = get_object_or_404(Pruefer, pk=request.POST['pruefer_id'])
    frage = get_object_or_404(Frage, pk=frage_id)

    try:
        has_scored = request.session['has_scored']
    except KeyError:
        has_scored = []

    if frage.pk in has_scored:
        messages.add_message(request, messages.WARNING, 'Du hast bereits den Score der Frage erhöht')
    elif len(has_scored) > 10:
        messages.add_message(request, messages.WARNING, 'Du kannst nicht mehr als 10 Fragen gehabt haben')
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
