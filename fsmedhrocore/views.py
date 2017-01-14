from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render


@login_required
def user_profile(request, username):
    user = get_object_or_404(User, username=username)

    context = {'user': user, 'ownprofile': (request.user == user)}

    return render(request, 'user_profile.html', context)

@login_required
def user_self_redirect(request):

    # view personal profile
    return redirect("%s/" % request.user.username)