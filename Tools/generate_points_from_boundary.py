import json
import numpy as np
import geojson
import geopy.distance
from scipy.spatial import ConvexHull
from shapely.geometry import shape, Point





#minimum area rectangle
def minimum_area_bounding_box(geojson_path, output_path):
    with open(geojson_path, 'r') as f:
        geojson_data = json.load(f)
    
    polygon = np.array(geojson_data["features"][0]["geometry"]["coordinates"][0])
    hull = ConvexHull(polygon)
    hull_points = polygon[hull.vertices]
    
    min_area = float('inf')
    best_rect = None
    for i in range(len(hull_points)):
        p1, p2 = hull_points[i], hull_points[(i+1) % len(hull_points)]
        edge_vector = p2 - p1
        angle = np.arctan2(edge_vector[1], edge_vector[0])
        
        rot_matrix = np.array([[np.cos(-angle), -np.sin(-angle)], [np.sin(-angle), np.cos(-angle)]])
        rotated_points = np.dot(hull_points - p1, rot_matrix.T)
        
        min_x, max_x = rotated_points[:, 0].min(), rotated_points[:, 0].max()
        min_y, max_y = rotated_points[:, 1].min(), rotated_points[:, 1].max()
        
        area = (max_x - min_x) * (max_y - min_y)
        if area < min_area:
            min_area = area
            best_rect = np.array([
                [min_x, max_y],
                [max_x, max_y],
                [max_x, min_y],
                [min_x, min_y],
                [min_x, max_y]
            ])
            best_angle = angle
            best_origin = p1
    
    inv_rot_matrix = np.array([[np.cos(best_angle), -np.sin(best_angle)], [np.sin(best_angle), np.cos(best_angle)]])
    bounding_box_coords = np.dot(best_rect, inv_rot_matrix.T) + best_origin
    
    bounding_box_coords = bounding_box_coords.tolist()
    
    bounding_box_geojson = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": {"name": "oriented_bounding_box"},
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [bounding_box_coords]
                }
            }
        ]
    }
    
    with open(output_path, 'w') as f:
        json.dump(bounding_box_geojson, f, indent=4)
    
    return bounding_box_geojson




# generating parallel rows


def calculate_distance(p1, p2):
    """Calculate geodesic distance between two points."""
    return geopy.distance.geodesic((p1[1], p1[0]), (p2[1], p2[0])).meters

def calculate_bearing(p1, p2):
    """Calculate the initial bearing from p1 to p2."""
    lat1, lon1 = np.radians(p1[1]), np.radians(p1[0])
    lat2, lon2 = np.radians(p2[1]), np.radians(p2[0])
    delta_lon = lon2 - lon1
    x = np.sin(delta_lon) * np.cos(lat2)
    y = np.cos(lat1) * np.sin(lat2) - np.sin(lat1) * np.cos(lat2) * np.cos(delta_lon)
    return (np.degrees(np.arctan2(x, y)) + 360) % 360  # Normalize

def generate_parallel_rows(boundary_json, num_points=100, row_spacing=2.1):
    """Generate multiple rows of points spaced along the shortest side."""
    polygon_coords = boundary_json["features"][0]["geometry"]["coordinates"][0][:-1]

    # Identify the longest and shortest sides
    sides = [(polygon_coords[i], polygon_coords[(i + 1) % len(polygon_coords)]) for i in range(len(polygon_coords))]
    longest_side = max(sides, key=lambda side: calculate_distance(*side))
    shortest_side = min(sides, key=lambda side: calculate_distance(*side))
    
    long_length = calculate_distance(*longest_side)
    short_length = calculate_distance(*shortest_side)
    short_bearing = calculate_bearing(*shortest_side)
    long_bearing = calculate_bearing(*longest_side)

    # Number of rows that fit along the longest side
    num_rows = int(long_length // row_spacing)
    
    # Generate multiple rows
    geojson_output = {"type": "FeatureCollection", "features": []}
    plant_id = 1

    for row in range(num_rows):
        # Shift start point along the longest side
        shift_distance = row * row_spacing
        row_start = geopy.distance.distance(meters=shift_distance).destination((longest_side[0][1], longest_side[0][0]), long_bearing)
        row_start = (row_start.longitude, row_start.latitude)
        
        # Generate points along the shortest side
        spacing = short_length / (num_points - 1)
        points = [
            (
                geopy.distance.distance(meters=spacing * i)
                .destination((row_start[1], row_start[0]), short_bearing)
                .longitude,
                geopy.distance.distance(meters=spacing * i)
                .destination((row_start[1], row_start[0]), short_bearing)
                .latitude
            )
            for i in range(num_points)
        ]

        # Append to GeoJSON
        for point in points:
            geojson_output["features"].append({
                "type": "Feature",
                "properties": {"plant_id": plant_id, "row_id": row + 1},
                "geometry": {"type": "Point", "coordinates": point}
            })
            plant_id += 1

    return geojson_output



def filter_points_outside_boundary(boundary_json_path, points_json_path, output_json_path):
    # Load boundary polygon
    with open(boundary_json_path, "r", encoding="utf-8") as f:
        boundary_data = json.load(f)
    
    boundary_polygon = shape(boundary_data["features"][0]["geometry"])

    # Load points
    with open(points_json_path, "r", encoding="utf-8") as f:
        points_data = json.load(f)

    filtered_features = []

    for feature in points_data["features"]:
        point = Point(feature["geometry"]["coordinates"])
        
        # Keep only points outside the boundary
        if boundary_polygon.contains(point):
            filtered_features.append(feature)

    # Create the new GeoJSON with filtered points
    filtered_geojson = {
        "type": "FeatureCollection",
        "features": filtered_features
    }

    # Save to output file
    with open(output_json_path, "w", encoding="utf-8") as f:
        json.dump(filtered_geojson, f, indent=4)

    print(f"Filtered points saved to {output_json_path}")

if __name__ == "__main__":

    original_boundary_path="boundary_generated_kd.geojson"
    rectangle_boundary_path="boundary_generated_kd_rectangle_smallest_area.geojson"
    final_generated_path="generated_parallel_rows.geojson"
    output_json_path = "filtered_points.geojson"

    

    minimum_area_bounding_box(original_boundary_path,rectangle_boundary_path)

#143
    with open(rectangle_boundary_path, "r") as f:
        boundary_json = json.load(f)

    result = generate_parallel_rows(boundary_json)

    with open(final_generated_path, "w") as f:
        json.dump(result, f, indent=4)

    print(f"GeoJSON file saved as {final_generated_path}")

    filter_points_outside_boundary(original_boundary_path, final_generated_path, output_json_path)
