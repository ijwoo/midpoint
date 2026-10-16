from django.urls import path
from .views import display_map
app_name = 'maps'


urlpatterns = [
    path('display-map/', display_map, name='display_map'),
]
