from datetime import timedelta
from typing import Optional

import pandas as pd
import plotly.express as px

from utils.visualization.base import VisualizationMode, visualize


def schedule_gant_chart_fig(schedule_dataframe: pd.DataFrame,
                            visualization: VisualizationMode,
                            fig_file_name: Optional[str] = None):
    """
    Creates and saves a gant chart of the scheduled tasks to the specified path
    :param fig_file_name:
    :param visualization:
    :param schedule_dataframe: Pandas DataFrame with the information about schedule
    """
    fig = px.timeline(schedule_dataframe, x_start="start", x_end="finish", y="idx", hover_name='task_name',
                      hover_data=["workers"],
                      title=f"{'Диаграмма Ганта проектных работ'}",
                      category_orders={'idx': list(schedule_dataframe.idx)},
                      text='task_name')
    fig.update_traces(textposition='outside')
    fig.update_yaxes(showticklabels=False, title_text='Проектные работы')
    fig.update_xaxes(range=[schedule_dataframe.loc[:, 'start'].min() - timedelta(days=2),
                            schedule_dataframe.loc[:, 'finish'].max() + timedelta(days=25)],
                     title_text='Дата')
    fig.update_layout(autosize=True, margin_autoexpand=True, font_size=12)

    return visualize(fig, mode=visualization, file_name=fig_file_name)
