from django.conf.urls import include, url
from .views import LocationAPI

urlpatterns = [
    # Examples:
    # url(r'^$', 'restaurant_fare.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^', LocationAPI.as_view()),

]
