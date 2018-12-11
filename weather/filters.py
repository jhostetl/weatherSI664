import django_filters
from weather.models import Cities, States, Countries, Continents, TempsHourly


class CityFilter(django_filters.FilterSet):

	state_name = django_filters.ModelChoiceFilter(
		field_name='state',
		label='State',
		queryset=States.objects.all().order_by('state_name'),
		lookup_expr='exact'
	)


	class Meta:
		model = Cities
		# form = SearchForm
		# fields [] is required, even if empty.
		fields = []
