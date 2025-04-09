import json
import pandas as pd

def filter_geojson_by_excel(geojson_path, excel_path, output_path):
    # Load GeoJSON
    with open(geojson_path, 'r') as f:
        geojson_data = json.load(f)

    # Load Excel file (assumes first sheet)
    excel_data = pd.read_excel(excel_path)

    # Get the unique block_id from the Excel file (assumes only one block_id present)
    target_block_id = excel_data['block_id'].unique()[0]

    # Filter GeoJSON features that match the block_name
    matching_features = [
        feature for feature in geojson_data['features']
        if feature['properties']['block_name'] == target_block_id
    ]

    # Group features by row_id
    features_by_row = {}
    for feature in matching_features:
        row_id = feature['properties']['row_id']
        features_by_row.setdefault(row_id, []).append(feature)

    # Prepare new filtered features list
    filtered_features = []

    # Iterate through each row group in the Excel
    for _, row in excel_data.iterrows():
        row_number = row['row_number']
        current_plant_count = row['current_plant_count']

        if row_number in features_by_row:
            # Sort the features by plant_id
            row_features = sorted(
                features_by_row[row_number],
                key=lambda x: x['properties']['plant_id']
            )
            # Keep only the features up to current_plant_count
            filtered_features.extend(row_features[:current_plant_count])

    # Construct new GeoJSON with the same structure
    new_geojson = {
        "type": "FeatureCollection",
        "name": geojson_data.get("name", "filtered"),
        "crs": geojson_data.get("crs"),
        "features": filtered_features
    }

    # Save to output file
    with open(output_path, 'w') as f:
        json.dump(new_geojson, f, indent=4)

    print(f"Filtered GeoJSON saved to {output_path}")




filter_geojson_by_excel("E:/plant_point_generate_using_boundary_json/mayacamas/21b_block_updated.geojson",
                       "E:/plant_point_generate_using_boundary_json/mayacamas/vine_count_report_21b.xlsx", 
                       "E:/plant_point_generate_using_boundary_json/mayacamas/21b_block_updated.geojson")
