"""
集計結果をサーバーごとにシート分けして Excel で出力。保存先は data/output。
"""
from datetime import datetime
import pandas as pd
import logging
from pathlib import Path
from loganalyzer.analyzer import analyze_df
from loganalyzer.logging_config import setup_logging

logger = logging.getLogger(__name__)

def export_result(df : pd.DataFrame):
    """
    解析済みデータをExcelファイルとして出力する関数

    出力用ディレクトリを作成する（存在しない場合）
    元のDataFrameをコピーしてから処理を行う（元データを変更せずvisualizerに渡すため）
    date列を「YYYY-MM-DD」形式の文字列に変換する
    サーバー名ごとにデータを分割し、Excelファイルとして保存する

    :param df: analyze_df関数で生成された解析済みデータ
    :return: なし
    """
    logger.info(f'Export started')
    df_copy = df.copy()
    try:
        df_copy['date'] = df_copy['date'].apply(lambda x: x.strftime('%Y-%m-%d'))
    except (KeyError, TypeError):
        logger.exception('Date column is invalid')

    output_dir = Path(__file__).parent.parent / 'data' / 'output'
    try:
        output_dir.mkdir(parents=True, exist_ok=True)
        today = datetime.today().strftime('%Y%m%d')

        for server_name, df_by_server in df_copy.groupby('server_name'):
            filename = output_dir / f'{server_name}_{today}.xlsx'
            logger.info(f'Exporting {server_name} data to {filename}')
            df_by_server.to_excel(
                filename,
                index = False,
                sheet_name = str(server_name),
                header = True
            )
            logger.info(f'{server_name} data exported')

    except (OSError, MemoryError) as e:
        logger.exception(f'Export failed:{e}')
        raise

    else:
        logger.info(f'Export completed')


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
        "server_name": ["s1", "s2", "s2", "s1", ],
        "level": ["INFO", "ERROR", "WARNING", "INFO", ],
        "cpu_usage": [30.5, 80.2, 55.0, 40.3, ],
        "memory_usage": [38.4, 84.2, 71.7, 40.3, ]
    }
    data = pd.DataFrame(data)
    df_analyzed = analyze_df(data)

    export_result(df_analyzed)
