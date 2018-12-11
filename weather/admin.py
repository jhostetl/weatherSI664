from django.contrib import admin
import weather.models as models
# Register your models here.


@admin.register(models.Continents)
class ContinentsAdmin(admin.ModelAdmin):
	fields = [
		'continent_name',
	]

	list_display = [
		'continent_name',
	]
	ordering = ['continent_name']

@admin.register(models.Countries)
class CountriesAdmin(admin.ModelAdmin):
	fields = [
		'country_name',
		'continent',
	]

	list_display = [
		'country_name',
		'continent',
	]
	ordering = ['country_name']

@admin.register(models.States)
class StatesAdmin(admin.ModelAdmin):
	fields = [
		'state_name',
		'country',
	]

	list_display = [
		'state_name',
		'country',
	]
	ordering = ['state_name']


@admin.register(models.Cities)
class CitiesAdmin(admin.ModelAdmin):
	fields = [
		'city_name',
		'state',
	]

	list_display = [
		'city_name',
		'state',
	]
	ordering = ['city_name']




@admin.register(models.TempsHourly)
class TempsHourlyAdmin(admin.ModelAdmin):
	fields = [
		'time_period',
		'temp',
		'city'
	]

	list_display = [
		'time_period',
		'temp',
		'city'
	]
	ordering = ['time_period']


@admin.register(models.Tags)
class TagsAdmin(admin.ModelAdmin):
	fields = [
		'tag_name',

	]

	list_display = [
		'tag_name',
		'city_display'
	]
	ordering = ['tag_name']



