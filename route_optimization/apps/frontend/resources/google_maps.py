# resources/google_maps.py
import requests
from PIL import Image, ImageTk
from io import BytesIO

def get_static_map(center, zoom=12, size=(600,400), markers=None, path=None, api_key=None, scale=1):
    """
    Devuelve un mapa estático de Google Maps como ImageTk.PhotoImage
    - center: "lat,lng" del centro del mapa
    - zoom: nivel de zoom
    - size: tuple (width, height)
    - markers: lista de tuplas [(lat,lng),...]
    - path: string "lat1,lng1|lat2,lng2|..." para dibujar ruta
    - api_key: tu Google API key
    - scale: escala del mapa
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
