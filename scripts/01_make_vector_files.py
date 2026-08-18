from bld_src import config
from bld_src.site_data import add_plot_geometries
import pandas as pd

## takes in Justin's BLD survey plot dataframe with lon,lat columns
## outputs a point gdf and a polygon gdf with crs 26918

def main():
    p = pd.read_excel(config.PLOT_LOCATIONS_JUSTIN)
    points, polys = add_plot_geometries(p)
    points.to_file(config.PLOT_POINTS)
    print(f'wrote points to {config.PLOT_POINTS}')
    polys.to_file(config.PLOT_POLYS)
    print(f'wrote polys to {config.PLOT_POLYS}')
    

if __name__ == "__main__":
    main()