"""
集計結果をもとに CPU/メモリ使用率の折れ線グラフとエラー件数の棒グラフを描画し、data/output に PNG で保存する。
"""
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
    """
    解析結果のDataFrameをもとにグラフを生成し、画像ファイルとして保存する関数

    出力用ディレクトリを作成する（存在しない場合）
    CPU使用率・メモリ使用率の推移グラフを生成する
    エラー件数の棒グラフを生成する
    date列の最小値・最大値から期間を取得し、分析期間・生成時タイムスタンプ付きのファイル名でPNG形式で保存する
    :param df: analyze_df関数で生成された解析済みデータ
    :return: なし
    """

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
    """
    CPU使用率およびメモリ使用率の推移グラフを作成する関数


    date列を横軸として折れ線グラフを作成する
    cpu_avg、memory_avg列を使用して使用率を可視化する
    ラベル、タイトル、レイアウトを設定する

    :param df: analyze_df関数で生成された解析済みデータ
    :return:作成されたFigureオブジェクトとAxesオブジェクト
    """


    logger.info('Generating usage plot')
    fig, ax = plt.subplots(figsize=(12, 6))
    for server_name, server_df in df.groupby('server_name'):
        ax.plot(server_df['date'], server_df['cpu_avg'], label=f'{server_name} CPU Usage')
        ax.plot(server_df['date'], server_df['memory_avg'], label=f'{server_name} Memory Usage')

    ax.set_xlabel('Date')
    ax.tick_params(axis='x', labelrotation=45)
    ax.set_ylabel('Usage(%)')
    ax.set_title('Average Daily Usage')
    ax.legend()
    fig.tight_layout()

    logger.info('Usage plot generated')
    return fig, ax


def make_errors_bar_plot(df: pd.DataFrame) -> (Figure, Axes):
    """
    日別エラー件数の棒グラフを作成する関数

    date列を横軸として棒グラフを作成する
    ERROR列を使用して日別エラー件数を表示する
    ラベル、タイトル、レイアウトを設定する

    :param df: analyze_df関数で生成された解析済みデータ
    :return: 作成されたFigureオブジェクトとAxesオブジェクト
    """


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


#ここからはテストです
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