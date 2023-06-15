# region imports generales
import pandas as pd
import matplotlib.pyplot as plt
# endregion



# region import mapas
import folium
from folium.plugins import FastMarkerCluster
# endregion



# region imports geo 1
import geopandas as gpd
import geopy
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
# endregion



# region code geo 1
locator = Nominatim(user_agent="myGeocoder")
location = locator.geocode("Champ de Mars, Paris, France")

print(location.address)
print("Latitude = {}, Longitude = {}".format(location.latitude, location.longitude))

df = pd.read_csv(fr"local-dev\addresses.csv")
df.head()

df['ADDRESS'] = df['Address1'].astype(str) + ',' + \
                df['Address3'] + ',' + \
                df['Address4'] + ',' + \
                df['Address5'] + ',' + ' Sweden'   

df.head()


geocode = RateLimiter(locator.geocode, min_delay_seconds=1)
df['location'] = df['ADDRESS'].apply(geocode)
df['point'] = df['location'].apply(lambda loc: tuple(loc.point) if loc else None)

df.head()

# split point column into latitude, longitude and altitude columns
df[['latitude', 'longitude', 'altitude']] = pd.DataFrame(df['point'].tolist(), index=df.index)
df.head()


localizador = Nominatim(user_agent="myGeocoder")
ubicacion = localizador.geocode("Calle Castillo, 23, Santa Cruz, Santa Cruz De Tenerife, Spain")

print(ubicacion.address)
print("Latitude = {}, Longitude = {}".format(ubicacion.latitude, ubicacion.longitude))
# endregion



# region imports geo 2
import requests
# endregion

# region code geo 2
# Replace YOUR_API_KEY with your actual API key. Sign up and get an API key on https://www.geoapify.com/ 
API_KEY = "06f9460c92f54a449298ac986adadd7f"

# Define the address to geocode
address = "Calle Castillo, 59, Santa Cruz, Santa Cruz De Tenerife, Spain"

# Build the API URL
url = f"https://api.geoapify.com/v1/geocode/search?text={address}&limit=1&apiKey={API_KEY}"

# Send the API request and get the response
response = requests.get(url)

# Check the response status code
if response.status_code == 200:
    # Parse the JSON data from the response
    data = response.json()

    # Extract the first result from the data
    result = data["features"][0]

    # Extract the latitude and longitude of the result
    latitude = result["geometry"]["coordinates"][1]
    longitude = result["geometry"]["coordinates"][0]

    print(f"Latitude: {latitude}, Longitude: {longitude}")
else:
    print(f"Request failed with status code {response.status_code}")
# endregion
