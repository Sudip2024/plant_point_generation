import json

def merge_geojson(file1, file2, output_file):
    """
    Merges two GeoJSON files into one.
    
    Parameters:
    file1 (str): Path to the first GeoJSON file.
    file2 (str): Path to the second GeoJSON file.
    output_file (str): Path to save the merged GeoJSON file.
    """
    # Load the first GeoJSON file
    with open(file1, 'r', encoding='utf-8') as f:
        geojson1 = json.load(f)
    
    # Load the second GeoJSON file
    with open(file2, 'r', encoding='utf-8') as f:
        geojson2 = json.load(f)
    
    # Merge features
    merged_features = geojson1["features"] + geojson2["features"]
    
    # Create merged GeoJSON structure
    merged_geojson = {
        "type": "FeatureCollection",
        "name": "plants",
        "crs": geojson1.get("crs", {}),
        "features": merged_features
    }
    
    # Save the merged GeoJSON file
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(merged_geojson, f, indent=4)
    
    print(f"Merged GeoJSON saved as {output_file}")

# Example usage
merge_geojson("E:/plant_point_generate_using_boundary_json/bentelenne/final_plant_points/Bettinelli_plant_points_KD_v1_filtered.geojson",
               "E:/plant_point_generate_using_boundary_json/bentelenne/final_plant_points/F10_block_plants_KD.geojson", 
               "E:/plant_point_generate_using_boundary_json/bentelenne/final_plant_points/Bettinelli_plant_points_KD_v1_filtered.geojson")







# import os
# import json
# from pathlib import Path

# def merge_geojson_files(folder_path, output_path):
#     merged = {
#         "type": "FeatureCollection",
#         "name": "merged_features",
#         "crs": {
#             "type": "name",
#             "properties": {
#                 "name": "urn:ogc:def:crs:EPSG::32610"
#             }
#         },
#         "features": []
#     }

#     folder = Path(folder_path)
#     geojson_files = folder.glob("*.geojson")

#     for file in geojson_files:
#         with open(file, 'r', encoding='utf-8') as f:
#             data = json.load(f)
#             if data.get("features"):
#                 merged["features"].extend(data["features"])

#     # Save merged GeoJSON
#     with open(output_path, 'w', encoding='utf-8') as f:
#         json.dump(merged, f, indent=4)

#     print(f"Merged GeoJSON saved to {output_path}")





# merge_geojson_files("E:/plant_point_generate_using_boundary_json/final_mayacamas_files",
#                      "E:/plant_point_generate_using_boundary_json/mayacamas/Mayacamas_original_plant_points_04_04_2025.geojson")
