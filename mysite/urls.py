from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseRedirect
from django.urls import path, include

# Use static() to add url mapping to serve static files during development (only)

urlpatterns = [
    url(r'^$', lambda r: HttpResponseRedirect('weather/')),
    url(r'^admin/', admin.site.urls),
    path('auth/', include('social_django.urls', namespace='social')),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), {'next_page': settings.LOGOUT_REDIRECT_URL},
         name='logout'),
    path('weather/api/rest-auth/', include('rest_auth.urls')),
	path('weather/api/rest-auth/registration/', include('rest_auth.registration.urls')),    
	path('api-auth/', include('rest_framework.urls')),
	path('weather/api/', include('api.urls')),
    url(r'^weather/', include('weather.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)