
import requests
from PIL import Image, ImageTk
from io import BytesIO

def get_static_map(center, zoom=12, size=(600,400), markers=None, path=None, api_key=None, scale=1):
    """
    Returns a Google Maps static map as an ImageTk.PhotoImage.

    Parameters:
    - center: string "lat,lng" for the map center
    - zoom: zoom level (integer)
    - size: tuple (width, height) in pixels
    - markers: list of tuples [(lat, lng), ...] for map markers
    - path: string "lat1,lng1|lat2,lng2|..." to draw a route line
    - api_key: your Google API key
    - scale: map scale (1 or 2)
    """
    base_url = "https://maps.googleapis.com/maps/api/staticmap?"
    
    params = {
        "center": center,
        "zoom": zoom,
        "size": f"{size[0]}x{size[1]}",
        "scale": scale,
        "key": api_key,
    }

    if markers:
        # Todos los markers en rojo
        marker_strs = [f"{lat},{lng}" for lat, lng in markers]
        params["markers"] = "|".join(marker_strs)

    if path:
        # Línea azul de grosor 3 conectando los stops
        params["path"] = f"color:blue|weight:3|{path}"

    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        img_data = BytesIO(response.content)
        img = Image.open(img_data)
        return ImageTk.PhotoImage(img)
    else:
        print("Error loading Google Static Map:", response.status_code)
        return None
