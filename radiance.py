from osgeo import gdal
import os


def gainbias(input_scene, gain, bias, output_scene):

    """
    Function to convert digtial numbers to TOA radiance.
    Uses the gain and bias method. To be used with reflective 
    or emissive bands.

    Params
    ------
    input_scene : str
        File path to Landsat scene (.TIF)
    
    gain : float
        Band specific rescaling gain factor (multiplicative).
    
    bias : float
        Band specific rescaling bias factor (additive).
    
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
    trg_ar = gain * src_ar + bias
    trg_ar[src_ar == no_data] = no_data

    # write radiance to band
    trg_band.WriteArray(trg_ar)

    # close handles
    trg_ds.FlushCache()
    trg_ds = None
    trg_band = None
    src_ds = None
    src_band = None


def scaling(input_scene, lmin, lmax, qcalmin, qcalmax, output_scene):

    """
    Function to convert digtial numbers to TOA radiance.
    Uses the spectral radiance scaling method. To be used 
    with reflective or emissive bands.

    Params
    ------
    input_scene : str
        File path to Landsat scene (.TIF)
    
    lmin : float
        Spectral radiance scale to qcalmin.
    
    lmax : float
        Spectral radiance scale to qcalmax.
    
    qcalmin : float
        The minimum quantized calibrated pixel value. Typically 1.

    qcalmax : float 
        The maximum quantized calibrated pixel value. Typically 255.

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
    trg_ar = ((lmax - lmin)/(qcalmax - qcalmin)) * (src_ar - qcalmin) + lmin
    trg_ar[src_ar == no_data] = no_data

    # write radiance to band
    trg_band.WriteArray(trg_ar)

    # close handles
    trg_ds.FlushCache()
    trg_ds = None
    trg_band = None
    src_ds = None
    src_band = None