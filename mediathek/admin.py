from django.contrib import admin
from .models import *
from django.utils.html import format_html
from django.core.urlresolvers import reverse


def best_abholbereit(modeladmin, request, queryset):
    queryset.update(status=Auftrag.BEARBEITET)
best_abholbereit.short_description = "als 'abholbereit' markieren"

def best_abgeschlossen(modeladmin, request, queryset):
    queryset.update(status=Auftrag.ABGESCHLOSSEN)
best_abgeschlossen.short_description = "als 'abgeschlossen' markieren"

def best_bezahlt(modeladmin, request, queryset):
    queryset.update(bezahlt=True)
best_bezahlt.short_description = "als 'bezahlt' markieren"


class AngebotInline(admin.StackedInline):
    model = Angebot
    fields = ('ware', 'preis')


@admin.register(Sammelbestellung)
class SammelbestAdmin(admin.ModelAdmin):
    model = Sammelbestellung
    list_display = ('bezeichnung', 'start', 'ende', 'abgeschlossen', 'zusammenfassung')
    inlines = [AngebotInline, ]

    def zusammenfassung(self, obj):
        return format_html(
            '<a class="button" href="{}">als .csv downloaden</a>',
            reverse('mediathek:sammelbest_zusammenfassung', args=[obj.pk]),
        )
    zusammenfassung.short_description = 'Zusammenfassung'
    zusammenfassung.allow_tags = True


class BestellungPositionInline(admin.StackedInline):
    model = BestellungPosition
    fields = ('angebot', 'anzahl')


@admin.register(Bestellung)
class BestellungAdmin(admin.ModelAdmin):
    model = Bestellung
    list_display = (
        'get_auf_id',
        'datum',
        'user',
        'get_user_last_name',
        'get_user_first_name',
        'get_bezahlbetrag',
        'bezahlt',
        'get_status_display')
    ordering = ('-datum', '-id',)
    inlines = [BestellungPositionInline, ]
    actions = [best_abholbereit, best_abgeschlossen, best_bezahlt, ]
    search_fields = ['=user__username', '=id', 'user__last_name', 'user__first_name']


@admin.register(Kunde)
class KundeAdmin(admin.ModelAdmin):
    model = Kunde
    list_display = ('get_user_last_name', 'get_user_first_name')
    search_fields = ['=user__username', '=id', 'user__last_name', 'user__first_name']


@admin.register(Einstellungen)
class ExampleModelAdmin(admin.ModelAdmin):

    model = Einstellungen

    def has_add_permission(self, request):
        # check if generally has add permission
        retval = super().has_add_permission(request)
        # set add permission to False, if object already exists
        if retval and Einstellungen.objects.exists():
            retval = False
        return retval


# Register your models here.
admin.site.register(Ware)
