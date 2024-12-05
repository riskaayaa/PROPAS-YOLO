import geopandas as gpd

def merge_overlapping_features(gdf, intersection_threshold=0.2):
    # Check for overlapping features
    overlapping_features = gpd.overlay(gdf, gdf, how='union', keep_geom_type=False)

    # Drop invalid geometries
    overlapping_features = overlapping_features[overlapping_features.is_valid]

    # Check if there are valid geometries
    if not overlapping_features.empty:
        # Calculate the area of each resulting feature
        overlapping_features['area'] = overlapping_features['geometry'].area

        # Identify features with more than 20% overlap
        condition = overlapping_features['area'] > intersection_threshold * gdf.area.iloc[0]
        features_to_merge = overlapping_features[condition]

        # Merge the overlapping features
        merged_geometry = features_to_merge.unary_union

        # Create a GeoDataFrame with the merged geometry
        result_gdf = gpd.GeoDataFrame(geometry=[merged_geometry])

        return result_gdf
    else:
        print("No valid geometries found.")
        return gpd.GeoDataFrame()

# Specify input and output paths
input_path = 'public/patch-temp/combined_file.geojson'
output_path = 'public/patch-temp/merged/kav2.shp'

# Read GeoJSON file into a GeoDataFrame
gdf = gpd.read_file(input_path)

# Apply the merge_overlapping_features function with a specified intersection threshold
result_gdf = merge_overlapping_features(gdf, intersection_threshold=0.2)

# Check if the result GeoDataFrame is not empty before saving
if not result_gdf.empty:
    # Save the result to a new shapefile
    result_gdf.to_file(output_path, driver='ESRI Shapefile')
    print("Merged file saved successfully.")
else:
    print("No valid geometries to save.")
