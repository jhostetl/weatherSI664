from weather.models import CityTags, Tags, TempsHourly, Cities, States, Countries, Continents
from rest_framework import response, serializers, status


'''class PlanetSerializer(serializers.ModelSerializer):

# 	class Meta:
# 		model = Planet
# 		fields = ('planet_id', 'planet_name', 'unsd_name')
'''


class CitySerializer(serializers.ModelSerializer):

	class Meta:
		model = Cities
		fields = ('city_id', 'city_name')

class TempsHourlySerializer(serializers.ModelSerializer):

	time_period = serializers.CharField(max_length=25)
	temp = serializers.FloatField(allow_null=False)
	city_id = serializers.IntegerField(allow_null=False)

	class Meta:
		model = TempsHourly
		fields = ('hourly_weather_id','time_period','temp','city_id')

	def create(self, validated_data):
		"""
		This method persists a new HeritageSite instance as well as adds all related
		countries/areas to the heritage_site_jurisdiction table.  It does so by first
		removing (validated_data.pop('heritage_site_jurisdiction')) from the validated
		data before the new HeritageSite instance is saved to the database. It then loops
		over the heritage_site_jurisdiction array in order to extract each country_area_id
		element and add entries to junction/associative heritage_site_jurisdiction table.
		:param validated_data:
		:return: site
		"""

		# print(validated_data)

		site = TempsHourly.objects.create(**validated_data)

		return site


	def update(self, instance, validated_data):
		# site_id = validated_data.pop('heritage_site_id')

		instance.time_period = validated_data.get(
			'time_period',
			instance.time_period
		)
		instance.temp = validated_data.get(
			'temp',
			instance.temp
		)


		instance.save()

		return instance

