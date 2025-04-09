import json

def convert_first_to_second(input_file, output_file):
    with open(input_file, 'r') as f:
        data = json.load(f)

    # Update CRS
    output_data = {
        "type": "FeatureCollection",
        "name": "plants",
        "crs": {
            "type": "name",
            "properties": {"name": "urn:ogc:def:crs:OGC:1.3:CRS84"}
        },
        "features": []
    }

    for feature in data['features']:
        properties = feature['properties']
        coordinates = feature['geometry']['coordinates']

        # Convert coordinates from UTM to Lat/Lon (assuming EPSG:32610 to WGS84)
        import pyproj
        transformer = pyproj.Transformer.from_crs("epsg:32610", "epsg:4326", always_xy=True)
        lon, lat = transformer.transform(coordinates[0], coordinates[1])

        # Create the new feature
        new_feature = {
            "type": "Feature",
            "properties": {
                "farm_id": "Bettinelli",
                "block_id": properties['block_name'],
                "plant_id": properties['plant_id'],
                "row_id": properties['row_id']
            },
            "geometry": {
                "type": "Point",
                "coordinates": [lon, lat]
            }
        }
        output_data['features'].append(new_feature)

    # Write to output JSON
    with open(output_file, 'w') as f:
        json.dump(output_data, f, indent=2)

# Example usage
convert_first_to_second(
    'E:/plant_point_generate_using_boundary_json/bentelenne/final_plant_points/F10_block_plants_filtered.geojson',
    'E:/plant_point_generate_using_boundary_json/bentelenne/final_plant_points/F10_block_plants_KD.geojson'
    )
