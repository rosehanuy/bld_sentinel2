from bld_src import config
import pandas as pd
import matplotlib.pyplot as plt

def site_health_metrics_line_plot(out_df, metrics_type):
    out_df['Site'] = out_df['Plot'].str.split('-').str[2].map(config.SITE_MAP)

    if metrics_type == 'burden':
        metrics = config.BURDEN_METRICS
    else:
        metrics = config.SEVERITY_METRICS

    #metrics = ['banded_mean_severity','curled_mean_severity','no_symptom_mean_severity'] 
    labels  = ['Banded', 'Curled','No Symptom']
    colors  = ['C0', 'C1','C2']
    years   = config.SURVEY_YEARS
    sites   = sorted(out_df['Site'].unique())

    fig, axes = plt.subplots(2, 5, figsize=(15, 6), sharex=True, sharey=False)
    axes = axes.ravel()

    for i, s in enumerate(sites):
        ax = axes[i]
        site = out_df[out_df['Site'] == s]
        for m, l, c in zip(metrics, labels, colors):
            # individual plots
            for _, g in site.groupby('Plot'):
                g = g.sort_values('year')
                ax.plot(g['year'], g[m], color=c, alpha=0.3, linewidth=0.9)
            # site median
            med = site.groupby('year')[m].median()
            ax.plot(med.index, med.values, color=c, marker='o', linewidth=2, label=l)
        ax.set_title(s, fontsize=10)
        ax.grid(False)

    # hide any leftover panels if a site is missing
    for j in range(len(sites), len(axes)):
        axes[j].set_visible(False)

    for ax in axes:
        ax.set_xticks(years)
    for ax in axes[-5:]:
        ax.set_xlabel('Year')
    for ax in axes[::5]:
        ax.set_ylabel('Plot burden')

    handles, lbls = axes[0].get_legend_handles_labels()
    fig.legend(handles, lbls, loc='upper center', bbox_to_anchor=(0.5, 0.98),
            ncol=len(labels), frameon=False,title='thin lines = plots, bold = site median')

    fig.suptitle(f'BLD Symptom {metrics_type.title()} by Site', y=1.0)
    plt.tight_layout(rect=[0, 0, 1, 0.93])
    plt.savefig(config.SAVE_FIGS / f'justin_plots_{metrics_type}_{config.SURVEY_YEARS[0]}_{config.SURVEY_YEARS[-1]}.png')