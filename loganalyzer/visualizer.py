import logging
import time
from pathlib import Path
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.figure import Figure
from matplotlib.axes import Axes
from loganalyzer.logging_config import setup_logging

logger = logging.getLogger(__name__)

def visualize_result(df: pd.DataFrame):

    logger.info('Visualizing result')
    output_dir = Path(__file__).parent.parent / 'data' / 'output'
    output_dir.mkdir(parents=True, exist_ok=True)

    try:
        start_date = df['date'].min().strftime('%Y-%m-%d')
        end_date = df['date'].max().strftime('%Y-%m-%d')
    except (KeyError, TypeError, ValueError, AttributeError) as e:
        logger.exception(f'Data error: {e}')
        raise

    now = str(int(time.time()))
    try:
        fig1, ax1 = make_usage_plot(df)
        fig1.savefig(output_dir / f'usage_{start_date}-{end_date}_{now}.png')

        fig2, ax2 = make_errors_bar_plot(df)
        fig2.savefig(output_dir / f'errors_{start_date}-{end_date}_{now}.png')

    except (KeyError, ValueError, TypeError) as e:
        logger.exception(f'Data error: {e}')
        raise
    except (OSError, MemoryError) as e:
        logger.exception(f'Plot saving failed: {e}')
        raise
    except Exception as e:
        logger.exception(f'Visualization failed: {e}')
        raise

    else:
        logger.info(f'Visualization completed')


def make_usage_plot(df: pd.DataFrame) -> (Figure, Axes):

    logger.info('Generating usage plot')
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(df['date'], df['cpu_avg'], label='CPU Usage')
    ax.plot(df['date'], df['memory_avg'], label='Memory Usage')

    ax.set_xlabel('Date')
    ax.tick_params(axis='x', labelrotation=45)
    ax.set_ylabel('Usage(%)')
    ax.set_title('Average Daily Usage')
    ax.legend()
    fig.tight_layout()

    logger.info('Usage plot generated')
    return fig, ax


def make_errors_bar_plot(df: pd.DataFrame) -> (Figure, Axes):

    logger.info('Generating errors bar plot')
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(df['date'], df['ERROR'], label='Daily Error Count')

    ax.set_xlabel('Date')
    ax.tick_params(axis='x', labelrotation=45)
    ax.set_ylabel('Count')
    ax.legend()
    fig.tight_layout()

    logger.info('Errors bar plot generated')
    return fig, ax


if __name__ == '__main__':
    setup_logging(level=logging.DEBUG)

    data = {
        "timestamp": pd.to_datetime([
            "2026-02-01 10:00:00",
            "2026-02-01 11:00:00",
            "2026-02-02 09:30:00",
            "2026-02-02 14:20:00",
        ]),
        "server_name": ["s1","s2","s2","s1",],
        "level": ["INFO","ERROR","WARNING","INFO",],
        "cpu_usage": [30.5,80.2,55.0,40.3,],
        "memory_usage": [38.4,84.2,71.7,40.3,]
    }
    data = pd.DataFrame(data)

    visualize_result(data)