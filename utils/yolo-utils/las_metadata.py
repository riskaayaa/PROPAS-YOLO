import laspy

def extract_las_extent(las_file):
    # Open the LAS file
    las = laspy.read(las_file)
    
    # Extract minimum and maximum values for X and Y coordinates
    min_x = las.header.min[0]
    min_y = las.header.min[1]
    
    max_x = las.header.max[0]
    max_y = las.header.max[1]
    
    return [min_x, min_y, max_x, max_y]

# # Example usage
# las_file = "datasets/Area_2.las"
# extent_values = extract_extent(las_file)
# print("Extent values:", extent_values)
