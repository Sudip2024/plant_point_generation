import geopandas as gpd
from shapely.geometry import LineString
import json

def generate_points_with_spacing(input_geojson_path, output_geojson_path, spacing_feet=5):
    # Load GeoJSON (in EPSG:4326)
    gdf = gpd.read_file(input_geojson_path)

    # Reproject to a CRS that uses feet (NAD83 / California zone III (ftUS))
    gdf = gdf.to_crs(epsg=2227)

    points = []

    for _, row in gdf.iterrows():
        row_id = row.get('row_id')
        line_geom = row.geometry

        # Flatten MultiLineString if needed
        if line_geom.geom_type == 'MultiLineString':
            line_geom = LineString([pt for part in line_geom.geoms for pt in part.coords])
        elif line_geom.geom_type != 'LineString':
            continue

        total_length = line_geom.length
        num_points = int(total_length // spacing_feet) + 1
        distances = [i * spacing_feet for i in range(num_points)]

        for i, dist in enumerate(distances):
            point = line_geom.interpolate(dist)
            points.append({
                "geometry": point,
                "row_id": row_id,
                "plant_id": i + 1
            })

    # Create GeoDataFrame from points
    points_gdf = gpd.GeoDataFrame(points, geometry="geometry", crs="EPSG:2227")

    # Reproject back to WGS84 for GeoJSON export
    points_gdf = points_gdf.to_crs(epsg=4326)

    # Export to GeoJSON
    points_gdf.to_file(output_geojson_path, driver="GeoJSON")
    print(f"Output saved to {output_geojson_path}")



generate_points_with_spacing(
    "E:/plant_point_generate_using_boundary_json/curved_row/curved_row.geojson", 
    "E:/plant_point_generate_using_boundary_json/curved_row/curved_row_points_v1.geojson"
    )
