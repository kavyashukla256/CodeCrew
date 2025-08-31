import requests
from django.http import JsonResponse
from .models import WeatherData, Alert
from .utils import check_risk, COASTAL_CITIES
from django.core.serializers import serialize
from django.http import HttpResponse

API_KEY = "77635d8dcf5501419fb5902a4ad9c0ee"
CITY = "dwarka"
URL = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"

# def fetch_weather(request):
#     response = requests.get(URL).json()

#     wind_speed = response['wind']['speed'] * 3.6   # convert m/s → km/h
#     rainfall = response.get('rain', {}).get('1h', 0)   # default 0 if no rain
#     tide_level = 3.0   # dummy for now

#     # save weather data
#     weather_entry = WeatherData.objects.create(
#         wind_speed=wind_speed,
#         rainfall=rainfall,
#         tide_level=tide_level
#     )

#     # check risk
#     level, message = check_risk(wind_speed, tide_level, rainfall)

#     # save alert
#     Alert.objects.create(level=level, message=message)

#     return JsonResponse({
#         "wind_speed": wind_speed,
#         "rainfall": rainfall,
#         "tide_level": tide_level,
#         "alert_level": level,
#         "alert_message": message
#     })

from .notifications import send_sms_alert, send_push_alert, add_fcm_token, remove_fcm_token

def fetch_weather(request):
    city = request.GET.get('city', 'dwarka').strip()
    if not city:
        city = 'dwarka'

    is_coastal = city.lower() in [c.lower() for c in COASTAL_CITIES]

    if is_coastal:
        # Fetch accurate current weather data
        URL = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        try:
            response = requests.get(URL).json()
            if response.get('cod') != 200:
                return JsonResponse({'error': 'City not found or API error'}, status=400)
            wind_speed = response['wind']['speed'] * 3.6   # convert m/s → km/h
            rainfall = response.get('rain', {}).get('1h', 0)   # default 0 if no rain
            tide_level = 3.0   # dummy for now
        except Exception as e:
            return JsonResponse({'error': 'Failed to fetch weather data'}, status=500)
    else:
        # Fetch rainfall prediction for non-coastal cities
        URL = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric"
        try:
            response = requests.get(URL).json()
            if response.get('cod') != '200':
                return JsonResponse({'error': 'City not found or API error'}, status=400)
            # Sum rainfall for next 24 hours (8 entries, 3h each)
            rainfall = sum(item.get('rain', {}).get('3h', 0) for item in response['list'][:8])
            # Estimate average wind speed from forecast data for next 24h
            wind_speed = sum(item['wind']['speed'] for item in response['list'][:8]) / 8 * 3.6  # m/s to km/h
            tide_level = 0   # no tide data for non-coastal
        except Exception as e:
            return JsonResponse({'error': 'Failed to fetch forecast data'}, status=500)

    # save weather data
    weather_entry = WeatherData.objects.create(
        wind_speed=wind_speed,
        rainfall=rainfall,
        tide_level=tide_level
    )

    # check risk
    level, message = check_risk(wind_speed, tide_level, rainfall)

    # save alert
    alert = Alert.objects.create(level=level, message=message)

    # send notifications if not GREEN and coastal
    if level != "GREEN" and is_coastal:
        send_sms_alert(f"[{level}] {message}")
        send_push_alert(message, title=f"ALERT: {level}")

    response_data = {
        "city": city,
        "is_coastal": is_coastal,
        "wind_speed": wind_speed,
        "rainfall": rainfall,
        "alert_level": level,
        "alert_message": message
    }
    if is_coastal:
        response_data.update({
            "tide_level": tide_level
        })

    return JsonResponse(response_data)


def get_alerts(request):
    alerts = Alert.objects.all().order_by('-created_at')[:10]  # last 10 alerts
    data = serialize("json", alerts)
    return HttpResponse(data, content_type="application/json")

def register_fcm_token(request):
    """API endpoint to register a new FCM token"""
    if request.method == 'POST':
        token = request.POST.get('token') or request.GET.get('token')
        if token:
            success = add_fcm_token(token)
            return JsonResponse({'success': success, 'message': 'Token registered successfully' if success else 'Token already exists'})
        return JsonResponse({'success': False, 'message': 'Token parameter is required'}, status=400)
    return JsonResponse({'success': False, 'message': 'Only POST method is allowed'}, status=405)

def unregister_fcm_token(request):
    """API endpoint to remove an FCM token"""
    if request.method == 'POST':
        token = request.POST.get('token') or request.GET.get('token')
        if token:
            success = remove_fcm_token(token)
            return JsonResponse({'success': success, 'message': 'Token removed successfully' if success else 'Token not found'})
        return JsonResponse({'success': False, 'message': 'Token parameter is required'}, status=400)
    return JsonResponse({'success': False, 'message': 'Only POST method is allowed'}, status=405)

def list_fcm_tokens(request):
    """API endpoint to list all registered FCM tokens (for debugging)"""
    from .notifications import VALID_FCM_TOKENS
    # Return only first 10 characters of each token for security
    masked_tokens = [token[:10] + '...' for token in VALID_FCM_TOKENS]
    return JsonResponse({'tokens': masked_tokens, 'count': len(VALID_FCM_TOKENS)})

from django.shortcuts import render

def weather_home(request):
    return render(request, "weather/index.html")
