# import csv
# import json

# def csv_to_geojson(csv_file, geojson_file, lat_col='Latitude', lon_col='Longitude'):
#     """
#     Converts a CSV file to a GeoJSON file.

#     :param csv_file: Path to the input CSV file.
#     :param geojson_file: Path to the output GeoJSON file.
#     :param lat_col: Name of the latitude column in CSV.
#     :param lon_col: Name of the longitude column in CSV.
#     """
#     geojson = {"type": "FeatureCollection", "features": []}
    
#     with open(csv_file, 'r', encoding='utf-8') as file:
#         reader = csv.DictReader(file)
#         for row in reader:
#             try:
#                 latitude = float(row[lat_col])
#                 longitude = float(row[lon_col])
#                 properties = {k: v for k, v in row.items() if k not in [lat_col, lon_col]}
#                 feature = {
#                     "type": "Feature",
#                     "geometry": {
#                         "type": "Point",
#                         "coordinates": [longitude, latitude]
#                     },
#                     "properties": properties
#                 }
#                 geojson["features"].append(feature)
#             except ValueError:
#                 print(f"Skipping row with invalid coordinates: {row}")
    
#     with open(geojson_file, 'w', encoding='utf-8') as file:
#         json.dump(geojson, file, indent=4)
    
#     return geojson_file

# # Example usage
# csv_to_geojson('bentelenne/Upper Range_20250228.csv',
#  'ground_control_points_bentelinne.geojson')







import pandas as pd
import geopandas as gpd
from shapely.geometry import Point

# Load CSV file
df = pd.read_csv("E:/plant_point_generate_using_boundary_json/mayacamas/Mayacamas GPS Points.csv")

# Drop rows where coordinates are missing
df = df.dropna(subset=["Latitude", "Longitude"])

# Create geometry column
geometry = [Point(xy) for xy in zip(df["Longitude"], df["Latitude"])]

# Convert to GeoDataFrame
gdf = gpd.GeoDataFrame(df, geometry=geometry)

# Set CRS (assuming WGS84 - EPSG:4326)
gdf.set_crs(epsg=4326, inplace=True)

# Save to GeoJSON
gdf.to_file("E:/plant_point_generate_using_boundary_json/mayacamas/Mayacamas_Groun_control_Points.geojson", driver="GeoJSON")
