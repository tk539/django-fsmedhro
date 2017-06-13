from django.contrib import admin

# Register your models here.
from .models import *


class StudiengangAdmin(admin.ModelAdmin):
    model = Studiengang
    filter_horizontal = ('studienabschnitt',)  # If you don't specify this, you will get a multiple select widget.


admin.site.register(Studiengang, StudiengangAdmin)
admin.site.register(Studienabschnitt)
admin.site.register(Fach)
admin.site.register(Gender)
admin.site.register(FachschaftUser)