from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django_filters.views import FilterView
from .models import Continents
from .models import Countries
from .models import States
from .models import Cities
from .models import TempsHourly
from .models import Tags
from .models import CityTags
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .forms import TempsHourlyForm
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.db.models import Max, Min, Avg
from django.db.models import Q
from weather.filters import CityFilter
from django.views import View
from django.db.models import F, Func




def index(request):
   return HttpResponse("Welcome!")

class HomePageView(generic.ListView):
	model = Cities
	context_object_name = 'cities'
	template_name = 'weather/home.html'

	def get_queryset(self):
		return Cities.objects.all().order_by('city_name')	
	

class TagView(generic.ListView):
	model = Tags
	context_object_name = 'tags'
	template_name = 'weather/tag.html'

	def get_queryset(self):
		return Tags.objects.all()

class TagCitiesView(generic.ListView):
	model = Tags
	context_object_name = 'tag_cities'
	template_name = 'weather/tag_cities.html'

	def get_context_data(self, **kwargs):
		pk = self.kwargs['pk']	
		sql_query_text = 'SELECT * FROM city_tags LEFT JOIN cities2 on cities2.city_id = city_tags.city_id LEFT JOIN states2 on states2.state_id = cities2.state_id LEFT JOIN countries2 on countries2.country_id = states2.country_id LEFT JOIN continents on continents.continent_id = countries2.continent_id LEFT JOIN tags on tags.tag_id = city_tags.tag_id WHERE city_tags.tag_id = '
		sql_query_text += str(pk)

		context_data = super().get_context_data(**kwargs)
		sql_query = CityTags.objects.raw(sql_query_text)

		context_data['queryset1'] = Tags.objects.filter(tag_id=pk)[0]
		context_data['queryset2'] = sql_query
		return context_data


class HourlyDetailView(generic.ListView):
	model = TempsHourly
	context_object_name = 'hourly_temps'
	template_name = 'weather/hourly_detail.html'

	def get_context_data(self, **kwargs):
		pk = self.kwargs['pk']
		context_data = super().get_context_data(**kwargs)
		context_data['queryset1'] = Cities.objects.filter(city_id=self.kwargs['city'])
		context_data['queryset2'] = TempsHourly.objects.filter(hourly_weather_id = pk)

		context_data['context_hour'] = self.kwargs['pk']
		context_data['context_month'] = self.kwargs['month']
		context_data['context_city'] = self.kwargs['city']
		context_data['context_state'] = self.kwargs['state']
		context_data['context_country'] = self.kwargs['country']
		context_data['context_continent'] = self.kwargs['continent']

		return context_data




@method_decorator(login_required, name='dispatch')
class HourlyCreateView(generic.View):
	model = TempsHourly
	form_class = TempsHourlyForm
	success_message = "Temperature added successfully"
	template_name = 'weather/temp_new.html'
	# fields = '__all__' <-- superseded by form_class
	# success_url = reverse_lazy('heritagesites/site_list')

	def dispatch(self, *args, **kwargs):
		return super().dispatch(*args, **kwargs)

	def post(self, request):
		form = TempsHourlyForm(request.POST)
		if form.is_valid():
			site = form.save(commit=False)
			site.save()
			# for country in form.cleaned_data['country_area']:
			# 	HeritageSiteJurisdiction.objects.create(heritage_site=site, country_area=country)
			return redirect(site) # shortcut to object's get_absolute_url()
			# return HttpResponseRedirect(site.get_absolute_url())
		return render(request, 'weather/temp_new.html', {'form': form})

	def get(self, request):
		form = TempsHourlyForm()
		return render(request, 'weather/temp_new.html', {'form': form})


@method_decorator(login_required, name='dispatch')
class HourlyUpdateView(generic.UpdateView):
	model = TempsHourly
	form_class = TempsHourlyForm
	# fields = '__all__' <-- superseded by form_class
	context_object_name = 'hourly_temp'
	# pk_url_kwarg = 'site_pk'
	success_message = "Hourly Temp updated successfully"
	template_name = 'weather/temp_update.html'

	def dispatch(self, *args, **kwargs):
		return super().dispatch(*args, **kwargs)

	def form_valid(self, form):
		site = form.save(commit=False)
		# site.updated_by = self.request.user
		# site.date_updated = timezone.now()
		site.save()

		# Current country_area_id values linked to site

		return HttpResponseRedirect(site.get_absolute_url())
		# return redirect('heritagesites/site_detail', pk=site.pk)

	def get_context_data(self, **kwargs):
		pk = self.kwargs['pk']
		context_data = super().get_context_data(**kwargs)


		context_data['context_hour'] = self.kwargs['pk']
		context_data['context_month'] = self.kwargs['month']
		context_data['context_city'] = self.kwargs['city']
		context_data['context_state'] = self.kwargs['state']
		context_data['context_country'] = self.kwargs['country']
		context_data['context_continent'] = self.kwargs['continent']
		return context_data

@method_decorator(login_required, name='dispatch')
class HourlyDeleteView(generic.DeleteView):
	model = TempsHourly
	success_message = "Hourly Temp deleted successfully"
	success_url = reverse_lazy('home')
	context_object_name = 'hourly_temp'
	template_name = 'weather/temp_delete.html'

	def dispatch(self, *args, **kwargs):
		return super().dispatch(*args, **kwargs)

	def delete(self, request, *args, **kwargs):
		self.object = self.get_object()
		self.object.delete()
		return HttpResponseRedirect(self.get_success_url())

	def get_context_data(self, **kwargs):
		context_data = super().get_context_data(**kwargs)

		context_data['context_hour'] = self.kwargs['pk']
		context_data['context_month'] = self.kwargs['month']
		context_data['context_city'] = self.kwargs['city']
		context_data['context_state'] = self.kwargs['state']
		context_data['context_country'] = self.kwargs['country']
		context_data['context_continent'] = self.kwargs['continent']

		return context_data


class WeatherDetailView(generic.ListView):
	model = TempsHourly
	context_object_name = 'hourly_temps'
	template_name = 'weather/weather_detail.html'

	def get_context_data(self, **kwargs):
		pk = self.kwargs['month']
		if pk < 10:
			pk_search = "-0" + str(pk) + "-"
		else:
			pk_search = "-" + str(pk) + "-"
		city_url = self.kwargs['city']
		context_data = super().get_context_data(**kwargs)
		context_data['queryset1'] = Cities.objects.filter(city_id=city_url)
		context_data['queryset2'] = TempsHourly.objects.filter(city_id=city_url).filter(time_period__contains = pk_search).order_by('time_period')

		context_data['context_month'] = pk
		context_data['context_city'] = self.kwargs['city']
		context_data['context_state'] = self.kwargs['state']
		context_data['context_country'] = self.kwargs['country']
		context_data['context_continent'] = self.kwargs['continent']
		return context_data


class WeatherCityView(generic.ListView):
	model = TempsHourly
	context_object_name = 'hourly_temps'
	template_name = 'weather/weather_city.html'

	def get_context_data(self, **kwargs):
		# would do this differently in the future. would convert in database beforehand.

		pk = self.kwargs['city']

		context_data = super().get_context_data(**kwargs)
		context_data['queryset1'] = Cities.objects.filter(city_id=pk)
		
		context_data['queryset2'] = TempsHourly.objects.filter(city_id=pk).aggregate(Max('temp'))["temp__max"]	
		context_data['queryset3'] = TempsHourly.objects.filter(city_id=pk).aggregate(Min('temp'))["temp__min"]
		context_data['queryset4'] = round(TempsHourly.objects.filter(city_id=pk).aggregate(Avg('temp'))["temp__avg"])

		context_data['querysetM1'] = round(TempsHourly.objects.filter(time_period__contains = "-01-").filter(city_id=pk).aggregate(Avg('temp'))["temp__avg"])
		context_data['querysetM2'] = round(TempsHourly.objects.filter(time_period__contains = "-02-").filter(city_id=pk).aggregate(Avg('temp'))["temp__avg"])
		context_data['querysetM3'] = round(TempsHourly.objects.filter(time_period__contains = "-03-").filter(city_id=pk).aggregate(Avg('temp'))["temp__avg"])
		context_data['querysetM4'] = round(TempsHourly.objects.filter(time_period__contains = "-04-").filter(city_id=pk).aggregate(Avg('temp'))["temp__avg"])
		context_data['querysetM5'] = round(TempsHourly.objects.filter(time_period__contains = "-05-").filter(city_id=pk).aggregate(Avg('temp'))["temp__avg"])
		context_data['querysetM6'] = round(TempsHourly.objects.filter(time_period__contains = "-06-").filter(city_id=pk).aggregate(Avg('temp'))["temp__avg"])
		context_data['querysetM7'] = round(TempsHourly.objects.filter(time_period__contains = "-07-").filter(city_id=pk).aggregate(Avg('temp'))["temp__avg"])
		context_data['querysetM8'] = round(TempsHourly.objects.filter(time_period__contains = "-08-").filter(city_id=pk).aggregate(Avg('temp'))["temp__avg"])
		context_data['querysetM9'] = round(TempsHourly.objects.filter(time_period__contains = "-09-").filter(city_id=pk).aggregate(Avg('temp'))["temp__avg"])
		context_data['querysetM10'] = round(TempsHourly.objects.filter(time_period__contains = "-10-").filter(city_id=pk).aggregate(Avg('temp'))["temp__avg"])
		context_data['querysetM11'] = round(TempsHourly.objects.filter(time_period__contains = "-11-").filter(city_id=pk).aggregate(Avg('temp'))["temp__avg"])
		context_data['querysetM12'] = round(TempsHourly.objects.filter(time_period__contains = "-12-").filter(city_id=pk).aggregate(Avg('temp'))["temp__avg"])

		context_data['context_city'] = pk
		context_data['context_state'] = self.kwargs['state']
		context_data['context_country'] = self.kwargs['country']
		context_data['context_continent'] = self.kwargs['continent']

		sql_query_text = 'SELECT * FROM city_tags LEFT JOIN cities2 on cities2.city_id = city_tags.city_id LEFT JOIN tags on tags.tag_id = city_tags.tag_id WHERE city_tags.city_id = '
		sql_query_text += str(pk)
		context_data['queryset_tags'] = CityTags.objects.raw(sql_query_text)

		return context_data


class CityFilterView(FilterView):
	filterset_class = CityFilter
	template_name = 'weather/city_filter.html'



class CityAreaListView(generic.ListView):
	model = Cities
	context_object_name = 'cities'
	template_name = 'weather/city_area.html'

	def get_queryset(self):
		pk = self.kwargs['state']
		return Cities.objects.filter(state_id=pk).order_by('city_name')

class StateAreaListView(generic.ListView):
	model = States
	context_object_name = 'states'
	template_name = 'weather/state_area.html'

	def get_queryset(self):
		pk = self.kwargs['country']
		return States.objects.filter(country_id=pk).order_by('state_name')



class CountryAreaListView(generic.ListView):
	model = Countries
	context_object_name = 'countries'
	template_name = 'weather/country_area.html'

	def get_queryset(self):
		pk = self.kwargs['continent']
		return Countries.objects.filter(continent_id=pk).order_by('country_name')


class ContinentAreaListView(generic.ListView):
	model = Continents
	context_object_name = 'continents'
	template_name = 'weather/continent_area.html'

	def get_queryset(self):
		return Continents.objects.all().order_by('continent_name')




