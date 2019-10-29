#!/user/bin/python
import os 
dir_path = os.path.dirname(os.path.realpath(__file__))
print(dir_path)


import pyproj
import pandas as pd

# Example position data, should be somewhere in Germany
# x = 652954.1006
# y = 4774619.7919
# z = -2217647.7937
x = 4075539.89941  
y = 931735.27025 
z = 4801629.35185
ecef = pyproj.Proj(proj='geocent', ellps='WGS84', datum='WGS84')
lla = pyproj.Proj(proj='latlong', ellps='WGS84', datum='WGS84')
lon, lat, alt = pyproj.transform(ecef, lla, x, y, z, radians=False)

print(lat, lon, alt)

def geocentric_to_lat_lon(x, y, z):
  ecef = pyproj.Proj(proj='geocent', ellps='WGS84', datum='WGS84')
  lla = pyproj.Proj(proj='latlong', ellps='WGS84', datum='WGS84')
  lon, lat, alt = pyproj.transform(ecef, lla, x, y, z, radians=False)
  return(lon, lat, alt)

coordinates = pd.read_csv(dir_path + "/" +"geocentric_coordinate.csv")
coordinates["longitude"], coordinates["latitude"], coordinates["altitude"] = geocentric_to_lat_lon(coordinates["X"].values,coordinates["Y"].values,coordinates["Z"].values)

header = ["key", "name", "longitude",	"latitude"]
coordinates.to_csv(dir_path + "/" + "coordinates_lon_lat.csv",columns = header, index=False)

coordinates_json = pd.read_csv(dir_path + "/" + "coordinates_lon_lat.csv")

coordinates_json.to_json(dir_path + "/" + "coordinates_lon_lat.json", orient='records')
print(coordinates_json.to_json(orient='records'))
