from osgeo import gdal
import numpy as np
import os


def gainbias(input_scene, gain, bias, sun_elev, output_scene):

    """
    Function to convert digtial numbers to TOA reflectance.
    Uses the gain and bias method. To be used with reflective 
    bands.

    Params
    ------
    input_scene : str
        File path to Landsat scene (.TIF)
    
    gain : float
        Band specific rescaling gain factor (multiplicative).
    
    bias : float
        Band specific rescaling bias factor (additive).
    
    sun_elev : float
        Local sun elevation angle.
    
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

    # convert to relectance
    trg_ar = gain * src_ar + bias

    # correct for sun elevation angle
    trg_ar = trg_ar / np.sin(np.radians(sun_elev))

    trg_ar[src_ar == no_data] = no_data

    # write radiance to band
    trg_band.WriteArray(trg_ar)

    # close handles
    trg_ds.FlushCache()
    trg_ds = None
    trg_band = None
    src_ds = None
    src_band = None


def ref(input_scene, earth_sun_dist, sun_elev, esun, output_scene):

    """
    Function to convert TOA radiance to TOA reflectance. To be
    used with reflective bands.

    Params
    ------
    input_scene : str
        File path to Landsat scene (.TIF)
    
    earth_sun_dist : float
        Earth-Sun distance in astronomical units.
    
    sun_elev : float
        Local sun elevation angle.
    
    esun : float
        Mean solar exoatmospheric irradiances.
    
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

    # convert to relectance
    solar_zenith = 90 - sun_elev

    trg_ar = (np.pi * src_ar * earth_sun_dist**2) / esun * np.cos(np.radians(solar_zenith))

    # correct for sun elevation angle
    if sun_elev:
        trg_ar = trg_ar / np.sin(np.radians(sun_elev))

    trg_ar[src_ar == no_data] = no_data

    # write radiance to band
    trg_band.WriteArray(trg_ar)

    # close handles
    trg_ds.FlushCache()
    trg_ds = None
    trg_band = None
    src_ds = None
    src_band = None