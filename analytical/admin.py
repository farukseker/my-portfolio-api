from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from analytical.models import ViewModel, AnalyticMedia
from unfold.contrib.import_export.forms import ExportForm
from unfold.admin import ModelAdmin
from import_export.admin import ExportActionModelAdmin
from django.db.models import Q


class CityCountryFilter(admin.SimpleListFilter):
    title = _("City / Country")
    parameter_name = "location"

    def lookups(self, request, model_admin):
        return [
            ("city", _("City Exists")),
            ("country", _("Country Exists")),
        ]

    def queryset(self, request, queryset):
        if self.value() == "City":
            return queryset.filter(~Q(ip_data__city=None))
        if self.value() == "Country":
            return queryset.filter(~Q(ip_data__country=None))
        return queryset


@admin.register(ViewModel)
class ViewModelAdmin(ModelAdmin, ExportActionModelAdmin):
    export_form_class = ExportForm
    list_display = ("ip_address", "visit_time", "request_type", "is_i_am")
    search_fields = ("ip_address", "user_agent", "ip_data__city", "ip_data__country")
    list_filter = ("request_type", CityCountryFilter)
