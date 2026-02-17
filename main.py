"""
ログ解析ツールのエントリポイント。ログ読込・解析・集計・Excel出力・グラフ生成を行う。
"""
import logging
from pathlib import  Path
from typing import Union
from loganalyzer.loader import load_logs_from_dir
from loganalyzer.logging_config import setup_logging
from loganalyzer.parser import parse_all
from loganalyzer.analyzer import analyze_df
from loganalyzer.exporter import export_result
from loganalyzer.visualizer import visualize_result

def main(data_dir : Path, log_dir : Union[Path, None] = None, level = logging.INFO):
    """
    運用ログを解析し、レポートおよびグラフを自動的に生成するツール

    処理フロー:
        1. 指定ディレクトリからログファイルを読み込む
        2. データのクレンジングと解析を実施
        3. サーバー別・日別に集計を行う
        4. Excel形式で集計結果を出力
        5. CPU＆メモリ使用率とエラー件数のグラフを生成・保存
        6. 処理中のエラーをにログに記録

    :param data_dir:　データ保存先のディレクトリのパス
    :param log_dir:　このプログラムのログ保存先のディレクトリのパス、指定しない場合はデフォルトパスを使用
    :param level: このプログラムのログのレベル、指定しない場合はデフォルトでlogging.INFOを使用
    :return: なし
    """

    data_dir = Path(data_dir)
    if not data_dir.exists():
        raise FileNotFoundError(f"{data_dir} does not exist")

    setup_logging(log_dir = log_dir, level = level)
    logger = logging.getLogger(__name__)

    logger.info('Process started')
    try:
        df_list, file_list = load_logs_from_dir(data_dir)
        parsed_df = parse_all(df_list, file_list)
        analyzed_df = analyze_df(parsed_df)

        export_result(analyzed_df)
        visualize_result(analyzed_df)

    except FileNotFoundError:
        raise
    except Exception as e:
        logger.exception(f'Process failed: {e}')
        raise

    logger.info('Process complete')


#ここからはテストです
if __name__ == '__main__':
    base_dir = Path(__file__).parent
    main(
        data_dir= base_dir / 'data' / 'sample_logs',
        log_dir= base_dir / 'logs',
        level=logging.INFO
    )