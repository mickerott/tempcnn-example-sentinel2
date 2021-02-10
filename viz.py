import numpy as np
from matplotlib.colors import ListedColormap, BoundaryNorm
from aenum import MultiValueEnum

class LULC(MultiValueEnum):
    """ Enum class containing basic LULC types
    """
    NO_DATA            = 'No Data',            0,  '#ffffff'
    CULTIVATED_LAND    = 'Cultivated Land',    1,  '#ffa500'
    FOREST             = 'Forest',             2,  '#054907'
    GRASSLAND          = 'Grassland',          3,  '#ffff00'
    SHRUBLAND          = 'Shrubland',          4,  '#806000'
    WATER              = 'Water',              5,  '#069af3'
    WETLAND            = 'Wetlands',           6,  '#95d0fc'
    TUNDRA             = 'Tundra',             7,  '#967bb6'
    ARTIFICIAL_SURFACE = 'Artificial Surface', 8,  '#dc143c'
    BARELAND           = 'Bareland',           9,  '#a6a6a6'
    SNOW_AND_ICE       = 'Snow and Ice',       10, '#000000'
    
    @property
    def id(self):
        """ Returns an ID of an enum type

        :return: An ID
        :rtype: int
        """
        return self.values[1]

    @property
    def color(self):
        """ Returns class color

        :return: A color in hexadecimal representation
        :rtype: str
        """
        return self.values[2]

def get_bounds_from_ids(ids):
    bounds = []
    for i in range(len(ids)):
        if i < len(ids) - 1:
            if i == 0:
                diff = (ids[i + 1] - ids[i]) / 2
                bounds.append(ids[i] - diff)
            diff = (ids[i + 1] - ids[i]) / 2
            bounds.append(ids[i] + diff)
        else:
            diff = (ids[i] - ids[i - 1]) / 2
            bounds.append(ids[i] + diff)
    return bounds
    
def get_colormap():
    return ListedColormap([x.color for x in LULC], name="lulc_cmap")

def get_boundarynorm():
    lulc_bounds = get_bounds_from_ids([x.id for x in LULC])
    lulc_cmap = get_colormap()
    return BoundaryNorm(lulc_bounds, lulc_cmap.N)

def normalize_img(img):
    new = []
    for i in range(img.shape[-1]):
        min_per, max_per = np.percentile(img[..., i], 2), np.percentile(img[..., i], 98)
        x = (img[..., i]-min_per) / (max_per-min_per)
        new.append(x)
    new = np.clip(np.stack(new, axis=-1), 0, 1)
    return new