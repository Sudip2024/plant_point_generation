import json

def filter_geojson(input_file, output_file, block_id):
    # Load the GeoJSON file
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Filter features based on block_id
    filtered_features = [feature for feature in data["features"] if feature["properties"].get("block_name") == block_id]
    
    # Create new GeoJSON structure with filtered features
    filtered_geojson = {
        "type": "FeatureCollection",
        "name": data.get("name", "filtered"),
        "crs": data.get("crs"),
        "features": filtered_features
    }
    
    # Save the filtered GeoJSON to a new file
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(filtered_geojson, f, indent=4)
    
    print(f"Filtered GeoJSON saved to {output_file}")

# Example usage
filter_geojson("E:/plant_point_generate_using_boundary_json/bentelenne/final_plant_points/F10_block_plants.geojson",
                "E:/plant_point_generate_using_boundary_json/bentelenne/final_plant_points/F10_block_plants_filtered.geojson", 
                "F10"
            )
