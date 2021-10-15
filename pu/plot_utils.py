import numpy as np
from bokeh.models import Band, ColumnDataSource


def add_hist_plot(x, plot, n_bins=100, x_range=None, **kwargs):
    if x_range is None:
        x_range = [min(x), max(x)]

    hist, edges = np.histogram(x, bins=n_bins, range=x_range)
    plot.quad(top=hist, bottom=0, left=edges[:-1], right=edges[1:], **kwargs)
    return plot


def err_plot(fig, x, y, y_err, fill_color='gray'):
    source = ColumnDataSource({'base': x, 'lower': y - y_err, 'upper': y + y_err})

    fig.circle(x, y, color='white', alpha=0)
    band = Band(base='base', lower='lower', upper='upper', source=source,
                level='underlay', fill_alpha=0.2, line_width=1,
                line_color='black', fill_color=fill_color)
    fig.add_layout(band)
