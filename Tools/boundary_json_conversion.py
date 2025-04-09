import json

def convert_second_to_first_boundary(input_file, output_file):
    with open(input_file, 'r') as f:
        data = json.load(f)

    # Update CRS
    output_data = {
        "type": "FeatureCollection",
        "name": "boundaries",
        "crs": {
            "type": "name",
            "properties": {"name": "urn:ogc:def:crs:OGC:1.3:CRS84"}
        },
        "features": []
    }

    for feature in data['features']:
        properties = feature['properties']
        
        # Create new feature with the required format
        new_feature = {
            "type": "Feature",
            "properties": {
                "block_name": properties['block_name'],
                "row_spacing": properties['row_space']
            },
            "geometry": {
                "type": feature['geometry']['type'],
                "coordinates": feature['geometry']['coordinates']
            }
        }
        output_data['features'].append(new_feature)

    # Write to output JSON
    with open(output_file, 'w') as f:
        json.dump(output_data, f, indent=2)
        print("done")

# Example usage
convert_second_to_first_boundary(
    'E:/plant_point_generate_using_boundary_json/bentelenne/final_boundary_file/F3_bettenelli.geojson', 
                                 
    'E:/plant_point_generate_using_boundary_json/bentelenne/final_boundary_file/F3_bettenelli_Kd.geojson'
)
