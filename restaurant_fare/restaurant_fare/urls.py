from django.conf.urls import include, url
from django.contrib import admin
from location import urls as location_urls
from location.views import LocationAPI, FareAPI

urlpatterns = [
    # Examples:
    # url(r'^$', 'restaurant_fare.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/v1/location/$', LocationAPI.as_view()),
    url(r'^api/v1/fare/(?P<lid>\d+)/$', FareAPI.as_view()),
]
