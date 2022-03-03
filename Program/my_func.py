import matplotlib.pyplot as plt
from skimage import io
import pickle
from osgeo import gdal, gdal_array
# Import OGR - 
from osgeo import ogr
import numpy as np
from helpers import *

def apply_model(model_fname, input_fname, output_fname, classes = 'all'):
    
    #read the model and load the model
    model = pickle.load(open(model_fname, 'rb'))
    
    #Read the image
    img_ds = gdal.Open(input_fname, gdal.GA_ReadOnly)
    img = np.zeros((img_ds.RasterYSize, img_ds.RasterXSize, img_ds.RasterCount),
               gdal_array.GDALTypeCodeToNumericTypeCode(img_ds.GetRasterBand(1).DataType))
    for b in range(img.shape[2]):
        img[:, :, b] = img_ds.GetRasterBand(b + 1).ReadAsArray()
        
    #Get transformation and projection info
    geo_transform = img_ds.GetGeoTransform()
    proj = img_ds.GetProjectionRef()
    
    #Image preprocessing: compute VIs
    
    #Reshape the image so that it can be fed into the model
    new_shape = (img.shape[0] * img.shape[1], img.shape[2])
    img_as_array = img[:, :, :4].reshape(new_shape)

  
    # Now predict for each pixel
    class_prediction = model.predict(img_as_array)
    # Reshape our classification map
    class_prediction = class_prediction.reshape(img[:, :, 0].shape)
    
    output = write_geotiff(output_fname, class_prediction, geo_transform, proj)
     #Export the classified image
    if classes == 'vitrified':
        mask_classified = class_prediction == 6
        output = write_geotiff(output_fname, mask_classified, geo_transform, proj)  
 
    return output


