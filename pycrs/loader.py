"""
Convenience functions for loading from different sources.
"""

import json
try:
    import urllib.request as urllib2
except ImportError:
    import urllib2
from . import parser


#################
# USER FUNCTIONS
#################

def from_url(url, format=None):
    """
    Returns the crs object from a string interpreted as a specified format, located at a given url site.

    Arguments:

    - *url*: The url where the crs string is to be read from. 
    - *format* (optional): Which format to parse the crs string as. One of "ogc wkt", "esri wkt", or "proj4".
        If None, tries to autodetect the format for you (default).

    Returns:

    - CRS object.
    """
    # first get string from url
    string = urllib2.urlopen(url).read()

    # then determine parser
    if format:
        # user specified format
        format = format.lower().replace(" ", "_")
        func = parser.__getattr__("from_%s" % format)
    else:
        # unknown format
        func = parser.from_unknown_text

    # then load
    crs = func(string)
    return crs

def from_file(filepath):
    """
    Returns the crs object from a file, with the format determined from the filename extension.

    Arguments:

    - *filepath*: filepath to be loaded, including extension. 
    """
    if filepath.endswith(".prj"):
        string = open(filepath, "r").read()
        return parser.from_esri_wkt(string)
    
    elif filepath.endswith((".geojson",".json")):
        raw = open(filepath).read()
        geoj = json.loads(raw)
        if "crs" in geoj:
            crsinfo = geoj["crs"]
            
            if crsinfo["type"] == "name":
                string = crsinfo["properties"]["name"]
                return parser.from_unknown_text(string)
                
            elif crsinfo["type"] == "link":
                url = crsinfo["properties"]["name"]
                type = crsinfo["properties"].get("type")
                return loader.from_url(url, format=type)
                
            else: raise Exception("invalid geojson crs type: must be either name or link")

        else:
            # assume default wgs84 as per the spec
            return parser.from_epsg_code("4326")

##    elif filepath.endswith((".tif",".tiff",".geotiff")):
##        pass
##        # ...




                                      
        
