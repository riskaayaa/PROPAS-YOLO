from osgeo import gdal, osr
from osgeo.gdalconst import GA_ReadOnly

class meta:
    def __init__(self, path:str):
        self.path = path

    def cari_extent(self):
        data = gdal.Open(self.path, GA_ReadOnly)
        geoTransform = data.GetGeoTransform()
        minx = geoTransform[0]
        maxy = geoTransform[3]
        maxx = minx + geoTransform[1] * data.RasterXSize
        miny = maxy + geoTransform[5] * data.RasterYSize
        ext = [minx, miny, maxx, maxy]
        data = None

        return ext
    
    def get_epsg_from_raster(self):
        # Open the raster file
        dataset = gdal.Open(self.path)

        if dataset is None:
            print(f"Error: Unable to open raster file {self.path}")
            return None

        # Get the raster's spatial reference
        spatial_ref = dataset.GetProjection()

        # Create a spatial reference object
        srs = osr.SpatialReference()
        srs.ImportFromWkt(spatial_ref)

        # Get the EPSG code
        epsg_code = srs.GetAttrValue('AUTHORITY', 1)

        dataset = None  # Close the dataset

        return epsg_code
    
    def calculate_area(self, coords):
        # Extract coordinates
        x1, y1, x2, y2 = coords

        # Calculate width and height
        width = abs(x2 - x1)
        height = abs(y2 - y1)

        # Calculate area
        area = width * height

        return area/10000
    
# a = meta('datasets/img/ortho_Kav2.tif').get_epsg_from_raster()
# b = meta('datasets/img/ortho_Kav2.tif').cari_extent()
# c = meta('datasets/img/ortho_Kav2.tif').calculate_area(b)

# c = "{:.2f}".format(c)

# print(a)
# print(b)
# print(f'{c} Ha')