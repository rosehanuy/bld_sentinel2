from shapely.geometry import Point
import geopandas as gpd
import pandas as pd
from bld_src import config
import numpy as np

def add_plot_geometries(p):
    
    geom = [Point(lon,lat) for lon, lat in zip(p['Longitude'],p['Latitude'])]
    geo_points = gpd.GeoDataFrame(p[['Site','Name']],geometry=geom,crs=4326  )
    geo_points = geo_points.to_crs(config.EPSG)

    # make polygons
    geo_polys = geo_points.copy()
    geo_polys['buffer'] = geo_polys.buffer(11.6)
    geo_polys = geo_polys.drop(columns='geometry').rename(columns={'buffer':'geometry'}).set_geometry('geometry')

    return geo_points, geo_polys


def get_plot_level_metrics():
    plot_col    = 'Plot'
    species_col = 'Species'
    species_code   = 'FAGR'
    ba_col      = 'ba_m2'                                  
    bld_metrics = ['no_symptom','banded','curled'] 
    dieback_col = 'Dieback Overall'  

    trees = pd.read_excel(config.HEALTH_DATA_JUSTIN,sheet_name=None)

    f = []
    for year in config.SURVEY_YEARS:

        df = trees[f'overstory_{year}']
        df = df.loc[df['Crown Class'].isin(['C','D'])].copy()
        df = df.rename(columns={'Normal Size No Symptom': 'no_symptom','Normal Size striped': 'banded','shrunken or curled':'curled'})

        df[ba_col] = config.BA_CONVERSION * (df["DBH"]**2)

        is_beech = df['Species'] == species_code

        ## code nonbeech as 0 for bld metrics
        df = df.fillna({m:0.0 for m in bld_metrics})

        # weight metrics by basal area
        for m in bld_metrics:
            df[f'{m}_weighted'] = np.where(is_beech,df[m]*df[ba_col],0.0)
        df['nonbeech_dieback_weighted'] = np.where(~is_beech,df[dieback_col]*df[ba_col],0.0)
        df['beech_ba'] = np.where(is_beech,df[ba_col],0.0)
        df['nonbeech_ba'] = np.where(~is_beech,df[ba_col],0.0)

        ## sum metrics per plot
        grouped = df.groupby(plot_col)
        out = pd.DataFrame({'total_ba':grouped[ba_col].sum(),
                        'beech_ba' : grouped['beech_ba'].sum(),
                            'nonbeech_ba': grouped['nonbeech_ba'].sum(),
                            'nonbeech_dieback': grouped['nonbeech_dieback_weighted'].sum(),
                            'n_beech': grouped[species_col].apply(lambda x: (x==species_code).sum()),
                            'n_nonbeech': grouped[species_col].apply(lambda x: (x!=species_code).sum())})
        for m in bld_metrics:
            out[m] = grouped[f'{m}_weighted'].sum()

        # beech abundance
        out['beech_rel_ba'] = out['beech_ba'] / out['total_ba']

        # weighted summed per-tree metrics divided by total plot basal area
        for m in bld_metrics:
            out[f'{m}_burden'] = out[m] / out['total_ba'] ## plot wide disease burden metric
            out[f'{m}_mean_severity'] = out[m] / out['beech_ba'] ## beech only severity metric

        out['nonbeech_dieback_burden'] = out['nonbeech_dieback'] / out['total_ba']

        out = out.reset_index()

        out['year'] = year

        f.append(out)

    return pd.concat(f)