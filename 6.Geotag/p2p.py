#Import packages
from osgeo import gdal
import os
import json
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import pyperclip
import re
from datetime import datetime
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import pyperclip
import re
import matplotlib.pyplot as plt

def get_gps_metadata_from_image(image_path):
    """Reads the EXIF data from an image file using GDAL.

    Args:
        image_path (str): The path to the image file.

    Returns:
        dict: A dictionary of EXIF data.
    """
    # Open the image file
    image = gdal.Open(image_path)

    # Get the image metadata
    metadata = image.GetMetadata()
    # if not metadata:
    #     raise ValueError("No EXIF metadata found")

    # Get the image EXIF tags
    gps_metadata = {key:metadata[key] for key in metadata.keys()}
    
    return gps_metadata

def get_decimal_from_dms(dms, ref):
    dms = re.findall(r'\d+\.?\d*', dms)
    dms = [float(num) for num in dms]
    degrees = dms[0]
    minutes = dms[1] / 60.0
    seconds = dms[2] / 3600.0

    if ref in ['S', 'W']:
        degrees = -degrees
        minutes = -minutes
        seconds = -seconds

    return round(degrees + minutes + seconds, 5)

def get_coordinates(geotags):
    lat = get_decimal_from_dms(geotags['EXIF_GPSLatitude'], geotags['EXIF_GPSLatitudeRef'])
    lon = get_decimal_from_dms(geotags['EXIF_GPSLongitude'], geotags['EXIF_GPSLongitudeRef'])
    alt = extract_number(geotags['EXIF_GPSAltitude'])

    return (lon,lat,alt)


def extract_number(s):
    if isinstance(s, str):
        numbers = re.findall(r"[-+]?\d*\.\d+|\d+", s)
        return float(numbers[0]) if numbers else None
    else:
        return s
    
if __name__ == '__main__':
    folder_path = pyperclip.paste()
    files = os.listdir(folder_path)
    data = []
    for file in files:
        try:
            if file.endswith(('.jpg', '.JPG')):  # add file types if needed.
                img_path = os.path.join(folder_path, file)
                geotagging = get_gps_metadata_from_image(img_path)
                coordinates = get_coordinates(geotagging)
                datetime = datetime.strptime(geotagging['EXIF_DateTime'],'%Y:%m:%d %H:%M:%S')
                data.append([file,img_path,geotagging])
        except:
            continue
    df = pd.DataFrame(data)
    df = pd.DataFrame(data, columns=['Name', 'Path','EXIF'])
    exif_df = pd.json_normalize(df['EXIF'])
    df = pd.concat([df, exif_df], axis=1)
    coordinates = df.apply(get_coordinates, axis=1)
    points = coordinates.apply(Point)
    gdf = gpd.GeoDataFrame(df, geometry=points,crs='EPSG:4326')
    columns_to_select = ['Name','Path','EXIF_DateTime','EXIF_FocalLengthIn35mmFilm',
        'EXIF_GPSImgDirection','EXIF_GPSImgDirectionRef','EXIF_Make',
        'EXIF_PixelXDimension', 'EXIF_PixelYDimension',
        'EXIF_SubjectArea','EXIF_XResolution', 'EXIF_YResolution',      
        'EXIF_GPSDOP','EXIF_SubjectDistance', 'EXIF_SubjectDistanceRange','geometry']
    for col in columns_to_select:
        # If the column does not exist in the DataFrame
        if col not in gdf.columns:
            # Add the column to the DataFrame with 'None' as the default value
            gdf[col] = None

    # Now select your columns
    gdf = gdf[columns_to_select]
    gdf['EXIF_GPSImgDirection'] = gdf['EXIF_GPSImgDirection'].apply(extract_number)
    gdf['EXIF_XResolution'] = gdf['EXIF_XResolution'].apply(extract_number)
    gdf['EXIF_YResolution'] = gdf['EXIF_YResolution'].apply(extract_number)
    gdf['EXIF_GPSDOP'] = gdf['EXIF_GPSDOP'].apply(extract_number)
    gdf['Pano'] = 1 if gdf['EXIF_Make'].str.contains('RICOH').any() else 0
    gdf['Type'] = '现状'
    gdf['Description'] = None
    gdf.to_file(os.path.join(folder_path,f'{os.path.basename(folder_path)}.json'),driver="GeoJSON")