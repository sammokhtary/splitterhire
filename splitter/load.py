from pathlib import Path
from django.contrib.gis.utils import LayerMapping
from .models import ServiceArea

servicearea_mapping = {
    'country': 'NAME_1',
    'area_name': 'NAME_2',
    'area_geom': 'MULTIPOLYGON',
}

uk_shp = Path(__file__).resolve().parent / 'data' / 'GBR_adm2.shp'

def run(verbose=True):
    lm = LayerMapping(ServiceArea, uk_shp, servicearea_mapping, transform=False)
    lm.save(strict=True, verbose=verbose)
