from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render
from fsmedhrocore.forms import UserForm, FachschaftUserForm
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages

def fachschaft_index(request):
    messages.add_message(request, messages.INFO, 'Hello World')
    return render(request, 'fsmedhrocore/index.html')


@login_required
def user_profile(request, username):
    user = get_object_or_404(User, username=username)

    try:
        fuser = user.fachschaftuser
    except ObjectDoesNotExist:
        fuser = None
        if request.user == user:
            # wenn eigenes profil, aber noch kein Fachschaft-Profil, dann bearbeiten/hinzufügen
            return redirect(user_edit)

    context = {'user': user, 'fuser': fuser, 'ownprofile': (request.user == user)}

    return render(request, 'fsmedhrocore/user_profile.html', context)


@login_required
def user_self_redirect(request):

    # view personal profile
    return redirect(user_profile, username=request.user.username)


@login_required
def user_edit(request):
    """
    context = {'user': request.user}
    if hasattr(request.user, 'fachschaftuser'):
        # Fachschaft-User schon vorhanden -> zum Profil
        return redirect('user_profile', username=request.user.username)
    else:
        # neuen Fachschaft-User anlegen
        return render(request, 'fsmedhrocore/user_edit.html', context)
    """

    if request.method == 'POST':
        uform = UserForm(data=request.POST, instance=request.user)
        try:
            # FachschaftUser bereits vorhanden?
            fuform = FachschaftUserForm(data=request.POST, instance=request.user.fachschaftuser)
        except ObjectDoesNotExist:
            fuform = FachschaftUserForm(data=request.POST)

        if uform.is_valid() and fuform.is_valid():
            user = uform.save()
            fuser = fuform.save(commit=False)
            fuser.user = user
            fuser.save()
            return redirect(user_profile, username=request.user.username)
    else:
        uform = UserForm(instance=request.user)

        try:
            # FachschaftUser bereits vorhanden?
            fuform = FachschaftUserForm(instance=request.user.fachschaftuser)
        except ObjectDoesNotExist:
            fuform = FachschaftUserForm()

    return render(request, 'fsmedhrocore/user_edit.html', {'user': request.user, 'uform': uform, 'fuform': fuform})