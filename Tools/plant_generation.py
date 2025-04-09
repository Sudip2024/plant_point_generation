from qgis.core import (
    QgsProject,
    QgsVectorLayer,
    QgsFeature,
    QgsPointXY,
    QgsGeometry,
    QgsField,
    QgsCoordinateReferenceSystem,
    QgsCoordinateTransform
)
from PyQt5.QtCore import QVariant
import math

# Load the block boundaries layer
layer_name = 'Mayacamas_22d_boundary'
blocks_layer = QgsProject.instance().mapLayersByName(layer_name)[0]

# Reproject the block boundaries layer to EPSG:32610
target_crs = QgsCoordinateReferenceSystem('EPSG:32610')
if blocks_layer.crs() != target_crs:
    transformer = QgsCoordinateTransform(blocks_layer.crs(), target_crs, QgsProject.instance())
    reprojected_layer = QgsVectorLayer(
        'Polygon?crs=EPSG:32610', 'blocks_reprojected', 'memory'
    )
    reprojected_layer_provider = reprojected_layer.dataProvider()
    
    # Add fields to the new reprojected layer
    reprojected_layer_provider.addAttributes(blocks_layer.fields())
    reprojected_layer.updateFields()
    
    # Transform features
    reprojected_features = []
    for feature in blocks_layer.getFeatures():
        geom = feature.geometry()
        geom.transform(transformer)  # Reproject geometry
        new_feature = QgsFeature()
        new_feature.setGeometry(geom)
        new_feature.setAttributes(feature.attributes())  # Copy attributes
        reprojected_features.append(new_feature)
    
    # Add reprojected features to the new layer
    reprojected_layer_provider.addFeatures(reprojected_features)
    QgsProject.instance().addMapLayer(reprojected_layer)
    blocks_layer = reprojected_layer  # Use reprojected layer going forward

# Create an output point layer for vines in EPSG:32610
output_layer = QgsVectorLayer('Point?crs=EPSG:32610', 'vine_points', 'memory')
output_layer_provider = output_layer.dataProvider()

# Add necessary fields to the output layer
output_layer_provider.addAttributes([
    QgsField('block_name', QVariant.String),
    QgsField('block_id', QVariant.Int),
    QgsField('row_id', QVariant.Int),
    QgsField('plant_id', QVariant.Int)
])
output_layer.updateFields()

# Conversion factor for feet to meters
feet_to_meters = 0.3048

# Helper function to rotate a point around a center
def rotate_point(x, y, cx, cy, angle_rad):
    dx = x - cx
    dy = y - cy
    x_rot = cx + dx * math.cos(angle_rad) - dy * math.sin(angle_rad)
    y_rot = cy + dx * math.sin(angle_rad) + dy * math.cos(angle_rad)
    return x_rot, y_rot

# Iterate through each block in the blocks layer
block_id = 1
for block in blocks_layer.getFeatures():
    block_name = block['block_name']
    plant_spacing = block['vine_space'] * feet_to_meters  # Convert feet to meters (horizontal)
    row_spacing = block['row_space'] * feet_to_meters  # Convert feet to meters (vertical)
    row_orientation = block['row_orient']  # Orientation in degrees

    # Adjust orientation for North as 0 and clockwise positive
    adjusted_angle = 90 - row_orientation  # Align rows with orientation
    if adjusted_angle < 0:
        adjusted_angle += 360
    angle_rad = math.radians(adjusted_angle)

    # Get the geometry of the block
    block_geom = block.geometry()

    # Calculate the block extent
    extent = block_geom.boundingBox()
    x_min, x_max = extent.xMinimum(), extent.xMaximum()
    y_min, y_max = extent.yMinimum(), extent.yMaximum()

    # Expand the grid area slightly to ensure full coverage
    buffer_factor = 1.5  # Expand the grid beyond the bounding box
    x_min -= (x_max - x_min) * buffer_factor
    x_max += (x_max - x_min) * buffer_factor
    y_min -= (y_max - y_min) * buffer_factor
    y_max += (y_max - y_min) * buffer_factor

    # Block center for rotation
    center = block_geom.centroid().asPoint()
    cx, cy = center.x(), center.y()

    # Reset row_id for the current block
    row_id = 1

    # Generate a larger grid of points
    y = y_min
    while y <= y_max:
        x = x_min

        # Reset plant_id for the current row
        plant_id = 1

        # Increment row_id for rows with at least one point inside the block
        row_has_points = False

        while x <= x_max:
            # Rotate the point around the block center
            x_rot, y_rot = rotate_point(x, y, cx, cy, angle_rad)

            # Check if the rotated point lies within the block
            point = QgsPointXY(x_rot, y_rot)
            if block_geom.contains(QgsGeometry.fromPointXY(point)):
                # Create a new feature for the point
                feature = QgsFeature()
                feature.setGeometry(QgsGeometry.fromPointXY(point))
                feature.setAttributes([block_name, block_id, row_id, plant_id])
                output_layer_provider.addFeature(feature)

                # Increment plant_id only if a point is created
                plant_id += 1
                row_has_points = True

            x += plant_spacing

        # Increment row_id if the row contains any points
        if row_has_points:
            row_id += 1

        y += row_spacing

    # Increment block_id for the next block
    block_id += 1

# Add the output layer to the QGIS project
QgsProject.instance().addMapLayer(output_layer)

print("Vine points generation with row and plant numbering reset completed!")






##################################################################



# from qgis.core import (
#     QgsProject,
#     QgsVectorLayer,
#     QgsFeature,
#     QgsPointXY,
#     QgsGeometry,
#     QgsField,
#     QgsCoordinateReferenceSystem,
#     QgsCoordinateTransform
# )
# from PyQt5.QtCore import QVariant
# import math

# # Load the block boundaries layer
# layer_name = 'c_blocks_all'
# blocks_layer = QgsProject.instance().mapLayersByName(layer_name)[0]

# # Reproject the block boundaries layer to EPSG:32610
# target_crs = QgsCoordinateReferenceSystem('EPSG:32610')
# if blocks_layer.crs() != target_crs:
#     transformer = QgsCoordinateTransform(blocks_layer.crs(), target_crs, QgsProject.instance())
#     reprojected_layer = QgsVectorLayer(
#         'Polygon?crs=EPSG:32610', 'blocks_reprojected', 'memory'
#     )
#     reprojected_layer_provider = reprojected_layer.dataProvider()
    
#     # Add fields to the new reprojected layer
#     reprojected_layer_provider.addAttributes(blocks_layer.fields())
#     reprojected_layer.updateFields()
    
#     # Transform features
#     reprojected_features = []
#     for feature in blocks_layer.getFeatures():
#         geom = feature.geometry()
#         geom.transform(transformer)  # Reproject geometry
#         new_feature = QgsFeature()
#         new_feature.setGeometry(geom)
#         new_feature.setAttributes(feature.attributes())  # Copy attributes
#         reprojected_features.append(new_feature)
    
#     # Add reprojected features to the new layer
#     reprojected_layer_provider.addFeatures(reprojected_features)
#     QgsProject.instance().addMapLayer(reprojected_layer)
#     blocks_layer = reprojected_layer  # Use reprojected layer going forward

# # Create an output point layer for vines in EPSG:32610
# output_layer = QgsVectorLayer('Point?crs=EPSG:32610', 'vine_points', 'memory')
# output_layer_provider = output_layer.dataProvider()

# # Add necessary fields to the output layer
# output_layer_provider.addAttributes([
#     QgsField('block_name', QVariant.String),
#     QgsField('block_id', QVariant.Int),
#     QgsField('row_id', QVariant.Int),
#     QgsField('plant_id', QVariant.Int)
# ])
# output_layer.updateFields()

# print([field.name() for field in blocks_layer.fields()])


# # Conversion factor for feet to meters
# feet_to_meters = 0.3048

# # Helper function to rotate a point around a center
# def rotate_point(x, y, cx, cy, angle_rad):
#     dx = x - cx
#     dy = y - cy
#     x_rot = cx + dx * math.cos(angle_rad) - dy * math.sin(angle_rad)
#     y_rot = cy + dx * math.sin(angle_rad) + dy * math.cos(angle_rad)
#     return x_rot, y_rot

# # Iterate through each block in the blocks layer
# block_id = 1
# for block in blocks_layer.getFeatures():
#     block_name = block['block_name']
#     plant_spacing = block['vine_space'] * feet_to_meters  # Convert feet to meters (horizontal)
#     row_spacing = block['row_space'] * feet_to_meters  # Convert feet to meters (vertical)
#     row_orientation = block['row_orient']  # Orientation in degrees
#       # Orientation in degrees

#     # Adjust orientation for North as 0 and clockwise positive
#     adjusted_angle = 270 - row_orientation  # Align rows with orientation
#     if adjusted_angle < 0:
#         adjusted_angle += 360
#     angle_rad = math.radians(adjusted_angle)

#     # Get the geometry of the block
#     block_geom = block.geometry()

#     # Calculate the block extent
#     extent = block_geom.boundingBox()
#     x_min, x_max = extent.xMinimum(), extent.xMaximum()
#     y_min, y_max = extent.yMinimum(), extent.yMaximum()

#     # Expand the grid area slightly to ensure full coverage
#     buffer_factor = 1.5  # Expand the grid beyond the bounding box
#     x_min -= (x_max - x_min) * buffer_factor
#     x_max += (x_max - x_min) * buffer_factor
#     y_min -= (y_max - y_min) * buffer_factor
#     y_max += (y_max - y_min) * buffer_factor

#     # Block center for rotation
#     center = block_geom.centroid().asPoint()
#     cx, cy = center.x(), center.y()

#     # Reset row_id for the current block
#     row_id = 1

#     # Generate a larger grid of points
#     y = y_min
#     while y <= y_max:
#         x = x_max

#         # Reset plant_id for the current row
#         plant_id = 1

#         # Increment row_id for rows with at least one point inside the block
#         row_has_points = False

#         while x >= x_min:
#             # Rotate the point around the block center
#             x_rot, y_rot = rotate_point(x, y, cx, cy, angle_rad)

#             # Check if the rotated point lies within the block
#             point = QgsPointXY(x_rot, y_rot)
#             if block_geom.contains(QgsGeometry.fromPointXY(point)):
#                 feature = QgsFeature()
#                 feature.setGeometry(QgsGeometry.fromPointXY(point))
#                 feature.setAttributes([block_name, block_id, row_id, plant_id])
#                 output_layer_provider.addFeature(feature)

#                 plant_id += 1
#                 row_has_points = True

#             x -= plant_spacing  # Decrement instead of increment
            

#         # Increment row_id if the row contains any points
#         if row_has_points:
#             row_id += 1

#         y += row_spacing

#     # Increment block_id for the next block
#     block_id += 1

# # Add the output layer to the QGIS project
# QgsProject.instance().addMapLayer(output_layer)

# print("Vine points generation with row and plant numbering reset completed!")