from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from analytical.models import ViewModel, IPRefModel, IPRequestMeta
from unfold.contrib.import_export.forms import ExportForm
from unfold.admin import ModelAdmin
from import_export.admin import ExportActionModelAdmin
from django.db.models import Q


class CityCountryFilter(admin.SimpleListFilter):
    title = _("City / Country")
    parameter_name = "location"

    def lookups(self, request, model_admin):
        return [
            ("ip__city", _("City Exists")),
            ("ip__country", _("Country Exists")),
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
    list_display = ("ip__ip_address", "ip__country", "ip__city", "visit_time")
    list_filter = (CityCountryFilter,)

admin.site.register(IPRefModel, ModelAdmin)
admin.site.register(IPRequestMeta, ModelAdmin)
