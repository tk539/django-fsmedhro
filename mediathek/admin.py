from django.contrib import admin
from .models import *


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
    list_display = ('bezeichnung', 'start', 'ende', 'abgeschlossen')
    inlines = [AngebotInline, ]


class BestellungPositionInline(admin.StackedInline):
    model = BestellungPosition
    fields = ('angebot', 'anzahl')


@admin.register(Bestellung)
class BestellungAdmin(admin.ModelAdmin):
    model = Bestellung
    list_display = ('datum', 'user_last_name', 'user_first_name', 'get_bezahlbetrag', 'bezahlt', 'get_status_display',)
    inlines = [BestellungPositionInline, ]
    actions = [best_abholbereit, best_abgeschlossen, best_bezahlt, ]

    def user_first_name(self, obj):
        return obj.user.first_name

    def user_last_name(self, obj):
        return obj.user.last_name

    user_first_name.admin_order_field = 'user__first_name'
    user_last_name.admin_order_field = 'user__last_name'


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
