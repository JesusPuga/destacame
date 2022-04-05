from django_filters import rest_framework as filters
from . import models


class TravelAvgFilter(filters.FilterSet):
    avg_seats_sold = filters.NumberFilter(method='filter_avg_seats_sold')

    class Meta:
        model = models.Travel
        fields = ['avg_seats_sold', 'travel_plan']

    def filter_avg_seats_sold(self, queryset, name, value):
        data = queryset.prefetch_related("journey_set")
        ids = []
        for element in data:
            seats_limit = element.bus.seats_amount if element.bus else 10
            if len(element.journey_set.all())/seats_limit*100 > value:
                ids.append(element.id)

        return queryset.filter(id__in = ids)