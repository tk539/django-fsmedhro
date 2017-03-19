from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404, redirect, render
from .models import Klausur, Fach, Frage, Kommentar
from fsmedhrocore.views import user_edit
from django.contrib import messages
from .forms import FrageForm
from django.http import HttpResponseRedirect
from django.urls import reverse


@login_required
def fachwahl(request):

    try:
        studiengang = request.user.fachschaftuser.studiengang
        Studienabschnitt = request.user.fachschaftuser.studienabschnitt
    except ObjectDoesNotExist:
        return redirect(user_edit)

    fach = Fach.objects.filter(
        active=True,
        Studienabschnitt=Studienabschnitt,
        Studiengang=studiengang
    ).order_by('name')

    if not fach.exists():
        messages.add_message(request, messages.INFO, 'Wir haben leider keine Fächer in deinem Studienabschnitt gefunden.')

    context ={'fach': Fach}

     #Wahl des Faches
    return render(request, 'QuestionAir/fachwahl.html', context)


@login_required
def klausurwahl(request):

    try:
        studiengang = request.user.fachschaftuser.studiengang
        Studienabschnitt = request.user.fachschaftuser.studienabschnitt
    except ObjectDoesNotExist:
        return redirect(user_edit)

    klausur = Klausur.objects.filter(
        active=True,
        Studienabschnitt=Studienabschnitt,
        Studiengang=studiengang
    ).order_by('name')

    if not Klausur.exists():
        messages.add_message(request, messages.INFO, 'Für dieses Fach ist keine Klausur abrufbar')

    context ={'Klausur': Klausur}

    return render(request, 'QuestionAir/klausurwahl.html',context)

#TODO: complete