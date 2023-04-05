from osgeo import gdal
import numpy as np
import os


def toa_rad_to_toa_bright(input_scene, k1, k2, output_scene):

    """
    Function to convert TOA radiance to TOA brightness (Kelvin).
    To be used with emissive bands. 

    Params
    ------
    input_scene : str
        File path to Landsat scene (.TIF)
    
    k1 : float
        Band specific calibration constant 1 (Kelvin).
    
    k2 : float
        Band specific calibration contstant 2 (W/(m2 sr um).
    
    output_scene : str
        File path to output scene (.TIF). File must not already 
        exist.

    Returns
    -------
    None
    """

    # ensure output does not already exist
    if os.path.exists(output_scene):
        raise ValueError(f"{output_scene} already exists!")
    
    # open source dataset
    src_ds = gdal.Open(input_scene)
    src_band = src_ds.GetRasterBand(1)

    # get source nodata value
    no_data = src_band.GetNoDataValue()

    # read in source array
    src_ar = src_band.ReadAsArray()

    # create target dataset
    drv = gdal.GetDriverByName("GTiff")
    trg_ds = drv.Create(
        output_scene, 
        src_ds.RasterXSize, 
        src_ds.RasterYSize, 
        1, 
        gdal.GDT_Float32
    )

    # set target metadata
    trg_ds.SetGeoTransform(src_ds.GetGeoTransform())
    trg_ds.SetProjection(src_ds.GetProjection())

    # get target band
    trg_band = trg_ds.GetRasterBand(1)

    # set target nodata value
    trg_band.SetNoDataValue(no_data)

    # convert to brightness
    trg_ar = k2 / np.log((k1 / src_ar) + 1)
    trg_ar[src_ar == no_data] = no_data

    # write radiance to band
    trg_band.WriteArray(trg_ar)

    # close handles
    trg_ds.FlushCache()
    trg_ds = None
    trg_band = None
    src_ds = None
    src_band = None


def dn_to_toa_bright(input_scene, gain, bias, k1, k2, output_scene):

    """
    Function to convert digital numbers to TOA brightness (Kelvin).
    To be used with emissive bands. 

    Params
    ------
    input_scene : str
        File path to Landsat scene (.TIF)
    
    k1 : float
        Band specific calibration constant 1 (Kelvin).
    
    k2 : float
        Band specific calibration contstant 2 (W/(m2 sr um).
    
    output_scene : str
        File path to output scene (.TIF). File must not already 
        exist.

    Returns
    -------
    None
    """

    # ensure output does not already exist
    if os.path.exists(output_scene):
        raise ValueError(f"{output_scene} already exists!")
    
    # open source dataset
    src_ds = gdal.Open(input_scene)
    src_band = src_ds.GetRasterBand(1)

    # get source nodata value
    no_data = src_band.GetNoDataValue()

    # read in source array
    src_ar = src_band.ReadAsArray()

    # create target dataset
    drv = gdal.GetDriverByName("GTiff")
    trg_ds = drv.Create(
        output_scene, 
        src_ds.RasterXSize, 
        src_ds.RasterYSize, 
        1, 
        gdal.GDT_Float32
    )

    # set target metadata
    trg_ds.SetGeoTransform(src_ds.GetGeoTransform())
    trg_ds.SetProjection(src_ds.GetProjection())

    # get target band
    trg_band = trg_ds.GetRasterBand(1)

    # set target nodata value
    trg_band.SetNoDataValue(no_data)

    # convert to radiance
    rad_ar = (gain * src_ar) + bias

    # convert to brightness
    bri_ar = k2 / np.log((k1 / rad_ar) + 1)
    bri_ar[src_ar == no_data] = no_data

    # write radiance to band
    trg_band.WriteArray(bri_ar)

    # close handles
    trg_ds.FlushCache()
    trg_ds = None
    trg_band = None
    src_ds = None
    src_band = None
