
import pandas

def plot_events(ax, df, start='start', end='end', color=None, annotate=None,
                label=None, alpha=0.2, zorder=-1,
                text_kwargs={}, **kwargs):

    """
    Plot events

    Uses vspan for events with duration, and vline for events with only start or end
    Can optionally add text annotations 
    """

    import itertools
    import seaborn
    palette = itertools.cycle(seaborn.color_palette())
    
    def valid_time(dt):
        return not pandas.isnull(dt)

    for idx, row in df.iterrows():
        s = row[start]
        e = row[end]
        
        if color is None:
            c = next(palette)
        else:
            c = row[color]
        
        if label is None:
            l = None
        else:
            l = row[label]

        if valid_time(s) and valid_time(e):
            ax.axvspan(s, e, label=l, color=c, alpha=alpha, zorder=zorder)
        if valid_time(e):
            ax.axvline(e, label=l, color=c, alpha=alpha, zorder=zorder)
        if valid_time(s):
            ax.axvline(s, label=l, color=c, alpha=alpha, zorder=zorder)

        import matplotlib.transforms
        trans = matplotlib.transforms.blended_transform_factory(ax.transData, ax.transAxes)
        if annotate is not None:
            ax.text(s, 1.05, row[annotate], transform=trans, **text_kwargs)


def legend_without_duplicate_labels(ax, loc='lower right', **kwargs):
    """
    Useful with plot_events() - because standard ax.legend() will get duplicates
    """
    handles, labels = ax.get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    ax.legend(by_label.values(), by_label.keys(), loc=loc, **kwargs)

