import geopandas as gpd
from shapely.geometry import LineString, Point
from scipy.interpolate import splprep, splev
import numpy as np

def smooth_line_with_bspline(line, smoothing=0):
    coords = np.array(line.coords)
    x, y = coords[:, 0], coords[:, 1]
    m = len(x)

    if m < 2:
        return line

    k = min(3, m - 1)
    try:
        tck, _ = splprep([x, y], s=smoothing, k=k)
        u_fine = np.linspace(0, 1, 500)
        x_smooth, y_smooth = splev(u_fine, tck)
        smooth_coords = list(zip(x_smooth, y_smooth))
        return LineString(smooth_coords)
    except Exception as e:
        print(f"[Warning] Failed to smooth line with {m} points: {e}")
        return line

def generate_points_on_smoothed_lines(input_geojson_path, output_points_path, spacing_feet=5, smoothing=0, output_smooth_line_path=None):
    gdf = gpd.read_file(input_geojson_path)
    gdf = gdf.to_crs(epsg=2227)

    points = []
    smoothed_lines = []

    for _, row in gdf.iterrows():
        row_id = row.get('row_id')
        geom = row.geometry

        if geom.geom_type == 'MultiLineString':
            geom = LineString([pt for part in geom.geoms for pt in part.coords])
        elif geom.geom_type != 'LineString':
            continue

        smooth_line = smooth_line_with_bspline(geom, smoothing=smoothing)

        # Store the smoothed line
        smoothed_lines.append({
            "geometry": smooth_line,
            "row_id": row_id
        })

        # Generate evenly spaced points
        total_length = smooth_line.length
        num_points = int(total_length // spacing_feet) + 1
        distances = [i * spacing_feet for i in range(num_points)]

        for i, dist in enumerate(distances):
            pt = smooth_line.interpolate(dist)
            points.append({
                "geometry": pt,
                "row_id": row_id,
                "plant_id": i + 1
            })

    # Export points
    points_gdf = gpd.GeoDataFrame(points, geometry="geometry", crs="EPSG:2227").to_crs(epsg=4326)
    points_gdf.to_file(output_points_path, driver="GeoJSON")
    print(f"Generated {len(points_gdf)} smoothed points → {output_points_path}")

    # Export smoothed lines (if requested)
    if output_smooth_line_path:
        smooth_gdf = gpd.GeoDataFrame(smoothed_lines, geometry="geometry", crs="EPSG:2227").to_crs(epsg=4326)
        smooth_gdf.to_file(output_smooth_line_path, driver="GeoJSON")
        print(f"Exported smoothed curves → {output_smooth_line_path}")


generate_points_on_smoothed_lines(
    "E:/plant_point_generate_using_boundary_json/curved_row/curved_row_v1.geojson", 
    "E:/plant_point_generate_using_boundary_json/curved_row/curved_row_points_smooth_v2_5.geojson",
    spacing_feet=4,
    smoothing=5, # Try 0 (interpolate exactly), or increase for more smoothing
    output_smooth_line_path="E:/plant_point_generate_using_boundary_json/curved_row/curved_row_curve_smooth_v2_5.geojson"
    )
