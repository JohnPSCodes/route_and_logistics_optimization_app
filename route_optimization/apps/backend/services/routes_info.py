import requests
from route_optimization.config_user import GOOGLE_API_KEY
from apps.backend.models import Route
from apps.backend.services.stops import get_route_stops

DIRECTIONS_URL = "https://maps.googleapis.com/maps/api/directions/json"

def get_route_driver(route_id):
    try:
        route = Route.objects.get(pk=route_id)
        if hasattr(route, "driver") and route.driver:
            return route.driver.user.name
    except Route.DoesNotExist:
        pass
    return "No asignado"

def get_route_stats(route_id):
    stops = get_route_stops(route_id)
    total_stops = len(stops)
    completed_stops = sum(1 for s in stops if s.delivered)

    # Solo las paradas pendientes se consideran para el cálculo de la ruta
    pending_stops = [s for s in stops if not s.delivered]

    locations = [(s.order.latitude, s.order.longitude) for s in pending_stops]
    return {
        "total_stops": total_stops,
        "completed_stops": completed_stops,
        "locations": locations
    }

def get_route_duration_and_distance(locations):
    """
    Calcula duración y distancia usando Google Directions API.
    Considera el orden de las paradas pendientes.
    """
    if len(locations) < 2:
        return {"duration_min": 0, "distance_km": 0, "duration_str": "0h 0m"}

    origin = f"{locations[0][0]},{locations[0][1]}"
    destination = f"{locations[-1][0]},{locations[-1][1]}"
    waypoints = "|".join([f"{lat},{lng}" for lat, lng in locations[1:-1]]) if len(locations) > 2 else None

    params = {
        "origin": origin,
        "destination": destination,
        "key": GOOGLE_API_KEY,
        "mode": "driving"
    }
    if waypoints:
        params["waypoints"] = waypoints

    response = requests.get(DIRECTIONS_URL, params=params)
    data = response.json()

    if not data.get("routes"):
        return {"duration_min": 0, "distance_km": 0, "duration_str": "0h 0m"}

    leg_list = data["routes"][0]["legs"]

    total_distance_m = sum(leg["distance"]["value"] for leg in leg_list)
    total_duration_s = sum(leg["duration"]["value"] for leg in leg_list)

    hours = total_duration_s // 3600
    minutes = (total_duration_s % 3600) // 60
    duration_str = f"{hours}h {minutes}m"

    return {
        "distance_km": round(total_distance_m / 1000, 2),
        "duration_min": round(total_duration_s / 60, 1),
        "duration_str": duration_str
    }

def get_full_route_info(route_id):
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
