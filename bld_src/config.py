from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

DATA_RAW = ROOT / 'data' / 'raw'
DATA_INTERIM = ROOT / 'data' / 'interim'
DATA_PROCESSED = ROOT / 'data' / 'processed'

SAVE_FIGS = ROOT / 'figs'

# raw inputs
PLOT_LOCATIONS_JUSTIN = DATA_RAW / 'BLD_all_plot_locations.xlsx'
HEALTH_DATA_JUSTIN = DATA_RAW / 'overstory_2023-2025.xlsx'

# derived
PLOT_POINTS = DATA_PROCESSED / 'justin_plots_points.gpkg'
PLOT_POLYS = DATA_PROCESSED / 'justin_plots_polygons.gpkg'

PLOT_HEALTH_METRICS = DATA_PROCESSED / 'justin_plots_health_metrics.csv'


# domain variables
SURVEY_YEARS = [2023,2024,2025]

EPSG = 26918
BA_CONVERSION = 0.00007854           # cm DBH -> m2 basal area

SITE_MAP = {
    'BRF':  'Black Rock Forest',
    'CVC':  'Catskills Visitor Center',
    'HP':   'Hillside Park',
    'MC':   'Marshlands Conservancy',
    'MP':   'Mohonk Preserve',
    'MTA':  'Mountaintop Arboretum',
    'NYBG': 'New York Botanical Garden',
    'RSP':  'Rockefeller State Park',
    'TR':   'Teatown Reservation',
    'VCP':  'Van Cortlandt Park',
}

BURDEN_METRICS = ['banded_burden', 'curled_burden','no_symptom_burden'] 
SEVERITY_METRICS = ['banded_mean_severity','curled_mean_severity','no_symptom_mean_severity']