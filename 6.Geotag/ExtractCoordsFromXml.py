
import xml.etree.ElementTree as ET
from pyproj import Transformer
import pyperclip
import pyperclip
import os

def new_func(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()

# Extract the SRS  from the XML
    source_srs = None
    for elem in root.iter():
        if 'SRS' in elem.tag:
            source_srs = elem.text
            break

# Extract the SRS origin coordinates from the XML
    srs_origin = None
    for elem in root.iter():
        if 'SRSOrigin' in elem.tag:
            srs_origin = elem.text
            break

# Assuming the coordinates are found and are in the format "x,y,z"
    if srs_origin:
        x, y, z = map(float, srs_origin.split(','))

    # Create a transformer object for converting from EPSG:4539 to EPSG:4326
        transformer = Transformer.from_crs(source_srs, "epsg:4326", always_xy=True)

    # Perform the transformation
        lon, lat, alt = transformer.transform(x, y, z)

    # Prepare the text to be copied to the clipboard
        clipboard_text = f"{lon}, {lat}, {alt}"
        pyperclip.copy(clipboard_text)
        print("Coordinates have been copied to the clipboard.")
    else:
        print("SRS Origin coordinates not found in the XML file.")

if __name__ == "__main__":
    # Get the file path from the clipboard
    file_path = pyperclip.paste()

    # Filter the XML files in the specified path
    xml_files = [file for file in os.listdir(file_path) if file.endswith('.xml')]
    if xml_files:
        for xml_file in xml_files:
            xml_file_path = os.path.join(file_path, xml_file)
            new_func(xml_file_path)
    else:
        print("No XML files found in the specified path.")
