from django_filters import FilterSet, CharFilter
from .models import Response


class ResponseFilter(FilterSet):
    announcement__heading = CharFilter(field_name='announcement__heading', lookup_expr='icontains',
                                                      label='Название объявления')

    class Meta:
        model = Response
        fields = ['announcement__heading']
