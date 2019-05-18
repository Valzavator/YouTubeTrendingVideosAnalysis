import os

import pandas as pd
import seaborn as sns
from pandas import DataFrame

from util.args import Args


def correlation(data: DataFrame, output_dir=Args.analysis_res_dir()):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    corr = data[['view_count', 'likes', 'dislikes', 'comment_count']].corr()
    plot = sns.heatmap(corr, cmap='Blues', annot=True)
    figure = plot.get_figure()
    figure.savefig(os.path.join(output_dir, 'correlation.png'))

