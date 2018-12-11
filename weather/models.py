# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.urls import reverse

class Continents(models.Model):
    continent_id = models.AutoField(primary_key=True)
    continent_name = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'continents'
        verbose_name = 'Continent'
        verbose_name_plural = 'Continents'

    def __str__(self):
        return self.continent_name


class Countries(models.Model):
    country_id = models.AutoField(primary_key=True)
    continent = models.ForeignKey(Continents, models.DO_NOTHING, blank=True, null=True)
    country_name = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'countries2'
        verbose_name = 'Country'
        verbose_name_plural = 'Countries'

    def __str__(self):
        return self.country_name


class States(models.Model):
    state_id = models.AutoField(primary_key=True)
    state_abbreviation = models.TextField(blank=True, null=True)
    state_name = models.TextField(blank=True, null=True)
    country = models.ForeignKey(Countries, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'states2'
        verbose_name = 'State'
        verbose_name_plural = 'States'

    def __str__(self):
        return self.state_name


class Cities(models.Model):
    city_id = models.AutoField(primary_key=True)
    city_name = models.TextField(blank=True, null=True)
    state = models.ForeignKey('States', models.DO_NOTHING, blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cities2'
        verbose_name = 'City'
        verbose_name_plural = 'Cities'

    def __str__(self):
        return self.city_name


class TempsHourly(models.Model):
    hourly_weather_id = models.AutoField(primary_key=True)
    city = models.ForeignKey(Cities, on_delete=models.CASCADE)

    time_period = models.CharField(blank=True, null=True, max_length=25)
    temp = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'hourly_weather5'
        verbose_name = 'Temp'
        verbose_name_plural = 'Temps'

    def get_absolute_url(self):
        month = self.time_period[5:7]
        return reverse('hourly_detail', kwargs={'pk': self.pk, 'month': month, 'city': self.city_id, 'state': self.city.state.state_id, 'country': self.city.state.country.country_id, 'continent': self.city.state.country.continent.continent_id})

    def __str__(self):
        return ("Temperature of {}".format(self.temp))


class Tags(models.Model):
    tag_id = models.AutoField(primary_key=True)
    tag_name = models.CharField(blank=True, null=True, max_length=245)
    city = models.ManyToManyField(Cities, through='CityTags')

    class Meta:
        managed = False
        db_table = 'tags'
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

    def __str__(self):
        return self.tag_name

    def city_display(self):
        """This is required to display in the Admin view."""
        return ', '.join(
            city.city_name for city in self.city.all())

class CityTags(models.Model):
    city_tags_id = models.AutoField(primary_key=True)
    city = models.ForeignKey(Cities, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tags, on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'city_tags'
        verbose_name = 'City Tag'
        verbose_name_plural = 'City Tags'





