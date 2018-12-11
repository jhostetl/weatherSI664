from django.urls import path

from . import views

urlpatterns = [
   path('', views.HomePageView.as_view(), name='home'),
   path('data/', views.ContinentAreaListView.as_view(), name='continents'),
   path('data/<int:continent>/', views.CountryAreaListView.as_view(), name='countries'), 
   path('data/<int:continent>/<int:country>/', views.StateAreaListView.as_view(), name='states'), 
   path('data/<int:continent>/<int:country>/<int:state>/', views.CityAreaListView.as_view(), name='cities'), 
   path('data/<int:continent>/<int:country>/<int:state>/<int:city>', views.WeatherCityView.as_view(), name='weather_city'), 
   path('data/<int:continent>/<int:country>/<int:state>/<int:city>/<int:month>', views.WeatherDetailView.as_view(), name='weather_detail'),
   path('data/<int:continent>/<int:country>/<int:state>/<int:city>/<int:month>/<int:pk>/', views.HourlyDetailView.as_view(), name='hourly_detail'),
   path('data/<int:continent>/<int:country>/<int:state>/<int:city>/<int:month>/<int:pk>/update/', views.HourlyUpdateView.as_view(), name='temp_update'),
   path('data/<int:continent>/<int:country>/<int:state>/<int:city>/<int:month>/<int:pk>/delete/', views.HourlyDeleteView.as_view(), name='temp_delete'),   
   path('data/new/', views.HourlyCreateView.as_view(), name='temp_new'),
   path('search/', views.CityFilterView.as_view(), name='search'),
   path('tags/', views.TagView.as_view(), name='tags'),
   path('tags/<int:pk>/', views.TagCitiesView.as_view(), name='tag_cities'),


]