import requests


API_KEY = "fa984a6a-1988-41b5-9d41-d01e284a14e2"

BASE_URL = "https://graphhopper.com/api/1/route"



def obtener_ruta(origen, destino):

   
    geo_url = "https://graphhopper.com/api/1/geocode"

   
    def geocode(ciudad):

        params = {
            "q": ciudad + ", Chile",
            "limit": 1,
            "key": API_KEY
        }

        resp = requests.get(geo_url, params=params)

        data = resp.json()

        if "message" in data:
            print("\nERROR API:")
            print(data["message"])
            return None

       
        if "hits" not in data or len(data["hits"]) == 0:
            print(f"\nNo se encontró la ciudad: {ciudad}")
            return None

        punto = data["hits"][0]["point"]

        return punto["lat"], punto["lng"]


    coord1 = geocode(origen)
    coord2 = geocode(destino)

    if coord1 is None or coord2 is None:
        return

    lat1, lng1 = coord1
    lat2, lng2 = coord2

  
    params = {
        "point": [f"{lat1},{lng1}", f"{lat2},{lng2}"],
        "vehicle": "car",
        "locale": "es",
        "instructions": True,
        "calc_points": True,
        "key": API_KEY
    }

    resp = requests.get(BASE_URL, params=params)

    data = resp.json()

   =
    if "paths" not in data:
        print("\nError obteniendo la ruta.")
        print(data)
        return

    path = data["paths"][0]

 
    distancia_km = path["distance"] / 1000

   
    duracion_ms = path["time"]

    duracion_s = duracion_ms / 1000

    horas = int(duracion_s // 3600)
    minutos = int((duracion_s % 3600) // 60)
    segundos = duracion_s % 60

   
    combustible = (distancia_km / 100) * 10

  
    instrucciones = path["instructions"]

    print(f"\n{'=' * 55}")
    print(f" Ruta: {origen} → {destino}")
    print(f"{'=' * 55}")

    print(f" Distancia:   {distancia_km:.2f} km")

    print(
        f" Duración:    "
        f"{horas:02d}h "
        f"{minutos:02d}m "
        f"{segundos:.2f}s"
    )

    print(f" Combustible: {combustible:.2f} litros")

  =
    print(f"\n --- Narrativa del viaje ---")

    for paso in instrucciones:

        texto = paso["text"]

        dist = paso["distance"] / 1000

        print(f" · {texto} ({dist:.2f} km)")

    print(f"{'=' * 55}\n")



print("=== Distancia fija: Santiago → Ovalle ===")

obtener_ruta("Santiago", "Ovalle")


===
while True:

    print("\nIngrese 'q' para salir.")

    origen = input("Ciudad de Origen: ").strip()

    if origen.lower() == "q":
        print("Saliendo del programa.")
        break

    destino = input("Ciudad de Destino: ").strip()

    if destino.lower() == "q":
        print("Saliendo del programa.")
        break

    obtener_ruta(origen, destino)