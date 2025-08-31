from django.urls import path
from .views import fetch_weather, get_alerts, register_fcm_token, unregister_fcm_token, list_fcm_tokens
from . import views


urlpatterns = [
    path('fetch/', fetch_weather),
    path('alerts/', get_alerts),
    path('fcm/register/', register_fcm_token),
    path('fcm/unregister/', unregister_fcm_token),
    path('fcm/tokens/', list_fcm_tokens),
    path("", views.weather_home, name="weather_home"),

]
# from django.urls import path
# from . import views

# urlpatterns = [
#     path("", views.weather_home, name="weather_home"),
# ]
