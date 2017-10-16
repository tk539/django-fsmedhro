from django.contrib import admin
from .models import *


def sb_abgeschlossen(modeladmin, request, queryset):
    queryset.update(abgeschlossen=True)
sb_abgeschlossen.short_description = "als 'abgeschlossen' markieren"


class AngebotInline(admin.TabularInline):
    model = Angebot


class SammelbestAdmin(admin.ModelAdmin):
    list_display = ('bezeichnung', 'start', 'ende', 'abgeschlossen')
    inlines = [
        AngebotInline,
    ]
    actions = [sb_abgeschlossen]


class BestellungAdmin(admin.ModelAdmin):
    model = Bestellung

# Register your models here.
admin.site.register(Sammelbestellung, SammelbestAdmin)
admin.site.register(Ware)
admin.site.register(Bestellung, BestellungAdmin)