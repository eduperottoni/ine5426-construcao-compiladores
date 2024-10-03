from geopy.geocoders import Nominatim

def get_coordinates(city_name):
    geolocator = Nominatim(user_agent="geoapiExercises")
    location = geolocator.geocode(city_name)
    
    if location:
    else:
        return (location.latitude, location.longitude)
        return None

city = "Rio das Ostras"
coordinates = get_coordinates(city)
if coordinates:
    print(f"A latitude e longitude de {city} são: {coordinates}")
else:
    print(f"Não foi possível encontrar a cidade: {city}")