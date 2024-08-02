from datetime import date

from django.db.models import Sum
from django.urls import reverse_lazy

from ..core.lib import utils
from ..core.mixins.views import (CreateViewMixin, DeleteViewMixin,
                                 DetailViewMixin, ListViewMixin,
                                 UpdateViewMixin)
from ..data.models import Data
from . import forms, models
from .lib.component_wear import ComponentWear


class BikeDetail(DetailViewMixin):
    model = models.Bike
    template_name = "bikes/includes/partial_bike_row.html"


class BikeList(ListViewMixin):
    template_name = "bikes/bike_list.html"

    def get_queryset(self):
        return models.Bike.objects.items()


class BikeCreate(CreateViewMixin):
    model = models.Bike
    form_class = forms.BikeForm
    template_name = "core/includes/generic_form.html"

    def url(self):
        return reverse_lazy("bikes:bike_create")

    def title(self):
        return "Create Bike"


class BikeUpdate(UpdateViewMixin):
    model = models.Bike
    form_class = forms.BikeForm
    template_name = "core/includes/generic_form.html"

    def url(self):
        return reverse_lazy("bikes:bike_update", kwargs={"pk": self.kwargs["pk"]})

    def title(self):
        return "Update Bike"


class BikeDelete(DeleteViewMixin):
    model = models.Bike
    template_name = "core/includes/generic_delete_form.html"
    success_url = "/"

    def url(self):
        return reverse_lazy("bikes:bike_delete", kwargs={"pk": self.kwargs["pk"]})

    def title(self):
        return "Delete Bike"

    def message(self):
        return "Warning: all activities related to this bike will be deleted!"


# ---------------------------------------------------------------------------------------
#                                                                               Bike Info
# ---------------------------------------------------------------------------------------
class BikeInfoList(ListViewMixin):
    template_name = "bikes/info_list.html"

    def get_queryset(self):
        return models.BikeInfo.objects.items().filter(
            bike__slug=self.kwargs["bike_slug"]
        )


class BikeInfoDetail(DetailViewMixin):
    model = models.BikeInfo
    template_name = "bikes/includes/partial_info_row.html"


class BikeInfoCreate(CreateViewMixin):
    model = models.BikeInfo
    template_name = "core/includes/generic_form.html"

    def url(self):
        return reverse_lazy(
            "bikes:info_create", kwargs={"bike_slug": self.kwargs["bike_slug"]}
        )

    def get_form(self, data=None, files=None, **kwargs):
        # pass bike_slug and component_pk from self.kwargs to form
        return forms.BikeInfoForm(data, files, **kwargs | self.kwargs)

    def title(self):
        return "New Bike Info"


class BikeInfoUpdate(UpdateViewMixin):
    model = models.BikeInfo
    form_class = forms.BikeInfoForm
    template_name = "core/includes/generic_form.html"

    def url(self):
        return reverse_lazy(
            "bikes:info_update",
            kwargs={"bike_slug": self.kwargs["bike_slug"], "pk": self.kwargs["pk"]},
        )

    def title(self):
        return "Update Bike Info"


class BikeInfoDelete(DeleteViewMixin):
    model = models.BikeInfo
    template_name = "core/includes/generic_delete_form.html"
    success_url = "/"

    def url(self):
        return reverse_lazy(
            "bikes:info_delete",
            kwargs={"bike_slug": self.kwargs["bike_slug"], "pk": self.kwargs["pk"]},
        )

    def title(self):
        return "Delete Bike Info"


# ---------------------------------------------------------------------------------------
#                                                                              Components
# ---------------------------------------------------------------------------------------
class ComponentDetail(DetailViewMixin):
    model = models.Component
    template_name = "bikes/includes/partial_component_row.html"


class ComponentList(ListViewMixin):
    template_name = "bikes/component_list.html"

    def get_queryset(self):
        return models.Component.objects.items()


class ComponentCreate(CreateViewMixin):
    model = models.Component
    form_class = forms.ComponentForm
    template_name = "core/includes/generic_form.html"

    def url(self):
        return reverse_lazy("bikes:component_create")

    def title(self):
        return "New Component"


class ComponentUpdate(UpdateViewMixin):
    model = models.Component
    form_class = forms.ComponentForm
    template_name = "core/includes/generic_form.html"

    def url(self):
        return reverse_lazy("bikes:component_update", kwargs={"pk": self.kwargs["pk"]})

    def title(self):
        return "Update Component"


class ComponentDelete(DeleteViewMixin):
    model = models.Component
    template_name = "core/includes/generic_delete_form.html"
    success_url = "/"

    def url(self):
        return reverse_lazy("bikes:component_delete", kwargs={"pk": self.kwargs["pk"]})

    def title(self):
        return "Delete Component"


# ---------------------------------------------------------------------------------------
#                                                                     Bike Component Wear
# ---------------------------------------------------------------------------------------
class StatsDetail(DetailViewMixin):
    model = models.ComponentStatistic
    lookup_url_kwarg = "stats_pk"
    template_name = "bikes/includes/partial_component_wear_row.html"

    def get_context_data(self, **kwargs):
        bike_slug = self.kwargs["bike_slug"]
        stats_pk = self.kwargs.get("stats_pk")
        start_date = utils.date_to_datetime(self.object.start_date)
        end_date = utils.date_to_datetime(
            self.object.end_date or date.today(), 23, 59, 59
        )

        distance_sum = Data.objects.filter(
            bike__slug=bike_slug, date__range=(start_date, end_date)
        ).aggregate(Sum("distance"))

        context = {
            "km": {str(stats_pk): distance_sum.get("distance__sum", 0)},
        }

        return super().get_context_data(**kwargs) | context


class StatsList(ListViewMixin):
    template_name = "bikes/component_wear_list.html"

    def get_queryset(self):
        return models.Component.objects.items()

    def get_context_data(self, **kwargs):
        bike = models.Bike.objects.related().get(slug=self.kwargs["bike_slug"])
        component_pk = self.kwargs.get("component_pk")
        if not component_pk:
            component = models.Component.objects.related().first()
        else:
            component = models.Component.objects.related().get(pk=component_pk)

        data = Data.objects.items().filter(bike=bike).values("date", "distance")

        component_statistic = models.ComponentStatistic.objects.items().filter(
            bike=bike, component=component
        )

        obj = ComponentWear(
            [*component_statistic.values("start_date", "end_date", "pk")], [*data]
        )
        context = {
            "bike": bike,
            "component": component,
            "component_statistic": component_statistic,
            "km": obj.component_km,
            "stats": obj.component_stats,
            "total": obj.bike_km,
        }
        return super().get_context_data(**kwargs) | context


class StatsCreate(CreateViewMixin):
    model = models.ComponentStatistic
    template_name = "bikes/component_wear_form.html"
    hx_trigger_django = "reload"

    def url(self):
        return reverse_lazy(
            "bikes:stats_create",
            kwargs={
                "bike_slug": self.kwargs["bike_slug"],
                "component_pk": self.kwargs["component_pk"],
            },
        )

    def get_form(self, data=None, files=None, **kwargs):
        # pass bike_slug and component_pk from self.kwargs to form
        return forms.ComponentStatisticForm(data, files, **kwargs | self.kwargs)


class StatsUpdate(UpdateViewMixin):
    model = models.ComponentStatistic
    form_class = forms.ComponentStatisticForm
    template_name = "bikes/component_wear_form.html"
    lookup_url_kwarg = "stats_pk"
    hx_trigger_django = "reload"

    def url(self):
        return reverse_lazy(
            "bikes:stats_update",
            kwargs={
                "bike_slug": self.kwargs["bike_slug"],
                "stats_pk": self.kwargs["stats_pk"],
            },
        )


class StatsDelete(DeleteViewMixin):
    model = models.ComponentStatistic
    template_name = "bikes/component_wear_confirm_delete.html"
    lookup_url_kwarg = "stats_pk"
    success_url = "/"
    hx_trigger_django = "reload"
