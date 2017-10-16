from django.contrib import admin
from .models import *


class AngebotInline(admin.TabularInline):
    model = Angebot

class SammelbestAdmin(admin.ModelAdmin):
    list_display = ('bezeichnung', 'start', 'ende', 'abgeschlossen')
    inlines = [
        AngebotInline,
    ]


# Register your models here.
admin.site.register(Sammelbestellung, SammelbestAdmin)
admin.site.register(Ware)