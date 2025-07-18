from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from .models import City, HydrologicalData, State

def calculate_monthly_data(data):
  months = [
    {'name': 'Jan', 'temp': 'temperature_average_january', 'precip': 'precipitation_average_january'},
    {'name': 'Fev', 'temp': 'temperature_average_february', 'precip': 'precipitation_average_february'},
    {'name': 'Mar', 'temp': 'temperature_average_march', 'precip': 'precipitation_average_march'},
    {'name': 'Abr', 'temp': 'temperature_average_april', 'precip': 'precipitation_average_april'},
    {'name': 'Mai', 'temp': 'temperature_average_may', 'precip': 'precipitation_average_may'},
    {'name': 'Jun', 'temp': 'temperature_average_june', 'precip': 'precipitation_average_june'},
    {'name': 'Jul', 'temp': 'temperature_average_july', 'precip': 'precipitation_average_july'},
    {'name': 'Ago', 'temp': 'temperature_average_august', 'precip': 'precipitation_average_august'},
    {'name': 'Set', 'temp': 'temperature_average_september', 'precip': 'precipitation_average_september'},
    {'name': 'Out', 'temp': 'temperature_average_october', 'precip': 'precipitation_average_october'},
    {'name': 'Nov', 'temp': 'temperature_average_november', 'precip': 'precipitation_average_november'},
    {'name': 'Dez', 'temp': 'temperature_average_december', 'precip': 'precipitation_average_december'},
  ]

  dry_months_count = 0
  monthly_data = []

  for month in months:
    temp_value = getattr(data, month['temp'], None)
    precip_value = getattr(data, month['precip'], None)
    precip_limit = 2 * float(temp_value) if temp_value else None
    condition = 'Seco' if precip_value and precip_value <= precip_limit else 'Chuvoso'

    monthly_data.append({
      'name': month['name'],
      'temp': temp_value,
      'precip': precip_value,
      'condition': condition,
    })

    if condition == 'Seco':
      dry_months_count += 1

  avg_temp = round(sum(getattr(data, month['temp'], 0) for month in months) / 12, 4)
  avg_precip = round(sum(getattr(data, month['precip'], 0) for month in months) / 12, 4)

  return monthly_data, dry_months_count, {'avg_temp': avg_temp, 'avg_precip': avg_precip}

def index(request):
  return render(request, 'index.html')

@require_GET
def get_cities(request):
  city_list = City.objects.all().order_by("station")
  cities_data = [{"id": city.id,"station": city.station} for city in city_list]
  return JsonResponse(cities_data, safe=False)
  
@require_GET
def get_states(request):
  states_list = State.objects.all().order_by("name")
  states_data = [{"id": state.id,"name": state.name} for state in states_list]
  return JsonResponse(states_data, safe=False)

@require_GET
def get_city(request, id):
  city_id = id;
  
  if not city_id:
    error_message = {"message": "id not passed"}
    return JsonResponse(error_message, status=400) 

  city = get_object_or_404(City, id=city_id)
  data = HydrologicalData.objects.filter(station=city).first()

  if not data:
    error_message = {"message": "city not exists"}
    return JsonResponse(error_message, status=400) 

  monthly_data, dry_months_count, averages = calculate_monthly_data(data)
  
  cities_data = {
    'monthly_data': monthly_data,
    'averages': averages,
    'dry_months_count': dry_months_count,
  }
  return JsonResponse(cities_data, safe=False)
  