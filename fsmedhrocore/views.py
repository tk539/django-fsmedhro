from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404, redirect, render


@login_required
def user_profile(request, username):
    user = get_object_or_404(User, username=username)
    context = {'user': user, 'ownprofile': (request.user == user)}

    return render(request, 'fsmedhrocore/user_profile.html', context)


@login_required
def user_self_redirect(request):

    # view personal profile
    return redirect('user_profile', username=request.user.username)


@login_required
def user_new(request):
    context = {'user': request.user}
    try:
        request.user.fachschaftuser
    except ObjectDoesNotExist:
        # neuen Fachschaft-User anlegen
        return render(request, 'fsmedhrocore/user_new.html', context)
    else:
        # Fachschaft-User schon vorhanden -> zum Profil
        return redirect('user_profile', username=request.user.username)
