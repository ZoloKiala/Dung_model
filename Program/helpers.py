from osgeo import gdal, gdal_array
# Import OGR - 
from osgeo import ogr
import numpy as np
import matplotlib.pyplot as plt

def write_geotiff(fname, data, geo_transform, projection):
    """Create a GeoTIFF file with the given data."""
    driver = gdal.GetDriverByName('GTiff')
    rows, cols = data.shape
    dataset = driver.Create(fname, cols, rows, 1, gdal.GDT_Byte)
    dataset.SetGeoTransform(geo_transform)
    dataset.SetProjection(projection)
    band = dataset.GetRasterBand(1)
    band.WriteArray(data)
    dataset = None  # Close the file
    
#Image preprocessing: compute VIs
def VI_computation (image):
    b_red = 2
    b_nir = 3

    ndvi = (image[:, :, b_nir] - image[:, :, b_red]) / (image[:, :, b_red] + image[:, :, b_nir])

    print(ndvi)
    print(ndvi.max())
