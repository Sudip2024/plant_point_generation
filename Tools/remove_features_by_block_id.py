import json

def remove_block_f9_features(geojson_data):
    """
    Removes features from the GeoJSON data where properties['block_id'] == 'F9'.

    Parameters:
        geojson_data (dict): The loaded GeoJSON as a Python dictionary.

    Returns:
        dict: The filtered GeoJSON dictionary.
    """
    filtered_features = [
        feature for feature in geojson_data.get("features", [])
        if feature.get("properties", {}).get("block_id") != "F10"
    ]
    geojson_data["features"] = filtered_features
    return geojson_data




# Load your GeoJSON from a file
with open("E:/plant_point_generate_using_boundary_json/bentelenne/final_plant_points/Bettinelli_plant_points_KD_v1.geojson", "r") as f:
    geojson = json.load(f)

# Filter out block F9 features
filtered_geojson = remove_block_f9_features(geojson)

# Save to a new file
with open("E:/plant_point_generate_using_boundary_json/bentelenne/final_plant_points/Bettinelli_plant_points_KD_v1_filtered.geojson", "w") as f:
    json.dump(filtered_geojson, f, indent=2)
