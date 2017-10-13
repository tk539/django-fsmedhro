from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test


def check_mediathek_mitarbeiter(user):
    return user.groups.filter(name='mediathek').exists()


@login_required
def mediathek_index(request):
    return render(request, 'mediathek/index.html')


@login_required
@user_passes_test(check_mediathek_mitarbeiter, login_url='mediathek:mediathek_index', redirect_field_name=None)
def mediathek_verwaltung(request):
    return render(request, 'mediathek/verwaltung.html')
