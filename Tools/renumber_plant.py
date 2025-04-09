import json
from collections import defaultdict

def reset_plant_ids(geojson_data):
    """
    Resets the plant_id values in the GeoJSON so that each block and row combination
    has plant_id values starting from 1 and incrementing sequentially.
    
    :param geojson_data: Dictionary representing the GeoJSON data.
    :return: Updated GeoJSON dictionary.
    """
    # Dictionary to keep track of plant_id sequences per (block_id, row_id)
    plant_counters = defaultdict(lambda: 1)
    
    # Iterate through features and update plant_id
    for feature in geojson_data["features"]:
        properties = feature["properties"]
        block_id = properties["block_id"]
        row_id = properties["row_id"]
        
        # Assign the sequential plant_id
        properties["plant_id"] = plant_counters[(block_id, row_id)]
        
        # Increment the counter for the next plant in the same block-row
        plant_counters[(block_id, row_id)] += 1
    
    return geojson_data

# Example usage
# Load the GeoJSON file
with open("E:/plant_point_generate_using_boundary_json/final_mayacamas_files/21a_block.geojson", "r") as f:
    geojson_data = json.load(f)

# Process the GeoJSON data
updated_geojson = reset_plant_ids(geojson_data)

# Save the updated GeoJSON file
with open("E:/plant_point_generate_using_boundary_json/final_mayacamas_files/21a_block.geojson", "w") as f:
    json.dump(updated_geojson, f, indent=4)
