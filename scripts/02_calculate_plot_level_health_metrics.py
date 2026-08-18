from bld_src import config
from bld_src.site_data import get_plot_level_metrics
from bld_src.viz import site_health_metrics_line_plot

# derives plot level health metrics from Justin's tree level health data
# calculates basal area from dbh
# weights health scores (0-6) by basal area (health scores for: dieback overall, banding, curling, no symptom)
# bld severity = sum of weighted beech health scores per plot / total beech basal area per plot
# bld burden = sum of weighted beech health scores per plot / total basal area per plot

# plot trajectories at each site

def main():
    out = get_plot_level_metrics()
    out.to_csv(config.PLOT_HEALTH_METRICS)
    print(f'wrote file to {config.PLOT_HEALTH_METRICS}')

    site_health_metrics_line_plot(out,metrics_type='severity')
    site_health_metrics_line_plot(out,metrics_type='burden')




if __name__ == "__main__":
    main()