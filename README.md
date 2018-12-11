# weatherSI664

Displays hourly weather data during 2016 for 36 cities.

Data set shows hourly weather from Kaggle.com, https://www.kaggle.com/selfishgene/historical-hourly-weather-data I only used the temperature data from 2016.

I created a structure to add future data for every country. It would be interesting to have more cities around the world. 

There is a many to many relationship between cities and tags. Others are one to many. Most cities don't have tags since they were manually assigned by me. My API and CRUD forms are for hourly temperature. This is a one to many. I finished my project before knowing that it should be a many to many.

Pagination wasn't working for me, but could have useful on the monthly temperature list pages. 

Below is the database model. 

![Database Model](https://github.com/jhostetl/weatherSI664/blob/master/weather/static/sql/weather-model.png)
