import requests
from route_optimization.config_user import GOOGLE_API_KEY
from apps.backend.models import Route
from apps.backend.services.stops import get_route_stops

DISTANCE_MATRIX_URL = "https://maps.googleapis.com/maps/api/distancematrix/json"

def get_route_driver(route_id):
    """Devuelve el nombre del conductor asignado a la ruta o 'No asignado' si no tiene."""
    try:
        route = Route.objects.get(pk=route_id)
        if hasattr(route, "driver") and route.driver:
            return route.driver.user.name
    except Route.DoesNotExist:
        pass
    return "No asignado"

def get_route_stats(route_id):
    """Devuelve estadísticas de la ruta: cantidad de stops, completados y ubicaciones."""
    stops = get_route_stops(route_id)
    total_stops = len(stops)
    completed_stops = sum(1 for s in stops if s.delivered)
    locations = [(s.order.latitude, s.order.longitude) for s in stops]
    return {
        "total_stops": total_stops,
        "completed_stops": completed_stops,
        "locations": locations
    }

def get_route_duration_and_distance(locations):
    """
    Calcula duración y distancia usando Distance Matrix API.
    locations: lista de tuplas (lat, lng)
    Devuelve diccionario con 'duration_min', 'distance_km' y 'duration_str'.
    """
    if len(locations) < 2:
        return {"duration_min": 0, "distance_km": 0, "duration_str": "0h 0m"}

    origins = "|".join([f"{lat},{lng}" for lat, lng in locations[:-1]])
    destinations = f"{locations[-1][0]},{locations[-1][1]}"

    params = {
        "origins": origins,
        "destinations": destinations,
        "key": GOOGLE_API_KEY,
        "mode": "driving"
    }

    response = requests.get(DISTANCE_MATRIX_URL, params=params)
    data = response.json()

    total_distance_m = 0
    total_duration_s = 0

    if data.get("rows"):
        for row in data["rows"]:
            for element in row.get("elements", []):
                if element.get("status") == "OK":
                    total_distance_m += element["distance"]["value"]
                    total_duration_s += element["duration"]["value"]

    # Convertir segundos a horas y minutos
    hours = total_duration_s // 3600
    minutes = (total_duration_s % 3600) // 60
    duration_str = f"{hours}h {minutes}m"

    return {
        "distance_km": round(total_distance_m / 1000, 2),
        "duration_min": round(total_duration_s / 60, 1),
        "duration_str": duration_str
    }

def get_full_route_info(route_id):
    """Devuelve toda la info de la ruta para mostrar en el panel."""
    stats = get_route_stats(route_id)
    driver = get_route_driver(route_id)
    duration_distance = get_route_duration_and_distance(stats["locations"])

    return {
        "driver": driver,
        "total_stops": stats["total_stops"],
        "completed_stops": stats["completed_stops"],
        "distance_km": duration_distance["distance_km"],
        "duration_min": duration_distance["duration_min"],
        "duration_str": duration_distance["duration_str"]
    }
