import numpy as np
import datetime


def earth_sun_dist(date, formula="Meeus"):

    """
    Function to calculate Earth-Sun distance for a given
    date. Earth-Sun distance will be expressed in terms
    of astronomical units or AU (mean distance from the center 
    of the Earth to the center of the sun).

    Params
    ------
    date : datetime.datetime
        datetime object

    formula : str
        String indicating which formula to use. Default is Meeus.
        Can be either Meeus, Spencer, Mather, ESA, or Duffie.

        Meeus: Meeus J (1998) Astronomical algorithms, 2nd Ed.
        Richmond, VA: Willmann-Bell. And DigitalGlobe
        https://dg-cms-uploads-production.s3.amazonaws.com/uploads/document/file/207/Radiometric_Use_of_WorldView-3_v2.pdf

        Spencer: Spencer JW (1971) Fourier series representation of 
        the position of the sun. Search 2/5. Taken from https://goo.gl/lhi9UI.
        
        Mather: Mather PM (2005) Computer Processing of Remotely-Sensed 
        An Introduction. Wiley: Chichester, ISBN: 978-0-470-02101-9, 
        https://eu.wiley.com/WileyCDA/WileyTitle/productCd-0470021012.html.

        ESA: ESA Earth Observation Quality Control: Landsat frequently asked questions. 

        Duffie: Duffie JA, Beckman WA (2013) Solar Engineering of Thermal 
        Processes. Wiley: Hoboken, New Jersey, ISBN: 978-0-470-87366-3,
        https://eu.wiley.com/WileyCDA/WileyTitle/productCd-0470873663.html.

    Returns
    -------
    float
    """

    if not isinstance(date, datetime.datetime):
        raise TypeError(f"Date must be of type {datetime.datetime}!")
    
    doy = date.timetuple().tm_yday

    if formula == "Meeus":
        if date.month <= 2:
            year = date.year - 1
            month = date.month + 12
        else:
            year = date.year
            month = date.month
        
        day = date.day
        ut = date.hour + (date.minute/60) + (date.second/3600)

        a = int(year/100)
        b = 2 - a + int(a/4)

        jd = int(365.25 * (year + 4716)) + int(30.6001 * (month + 1)) \
            + day + (ut/24.0) + b - 1524.5
        d = jd - 2451545.0
        g = np.radians(357.529 + 0.98560028 * d)

        return 1.00014 - 0.01671 * np.cos(g) - 0.00014 * np.cos(2*g)

    elif formula == "Spencer":
        p = 2 * np.pi * (doy - 1) / 365
        return (1/(1.000110 + 0.034221 * np.cos(p) + 0.001280 * np.sin(p) \
            + 0.000719 * np.cos(2 * p) + 0.000077 * np.sin(2 * p)))**0.5

    elif formula == "Mather":
        return 1/(1 - 0.016729 * np.cos(0.9856 * (doy - 4)))

    elif formula == "ESA":
        return 1 - 0.016729 * np.cos((2 * np.pi) * (0.9856 * (doy - 4) / 360))

    elif formula == "Duffie":
        return 1 + 0.033 * np.cos(doy * 2 * np.pi / 365)

    else:
        formulas = ["Meeus", "Spencer", "Mather", "ESA", "Duffie"]
        raise ValueError(f"Formula must be one of {formulas}!")
