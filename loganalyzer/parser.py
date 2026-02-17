"""
単一/複数ログファイルのクレンジングと結合。必須列チェック・欠損除去・日時変換・重複削除を行う。
"""
import pandas as pd
import logging
from pathlib import Path
from loganalyzer.logging_config import setup_logging

logger = logging.getLogger(__name__)

def parse_all(df_list : list[pd.DataFrame], file_list : list[Path]) -> pd.DataFrame:
    """
    複数ログファイルのデータをクレンジングし、一つにまとめる関数

    読み込まれた複数のDataFrameに対して順番にパース処理を行い、
    不正データの除外や形式統一などの前処理を実施する。

    個別ファイルの解析に失敗した場合はログに記録し、
    処理をスキップすることで全体処理への影響を最小限に抑える。

    有効なデータのみを統合し、1つのDataFrameとして返却する。

    :param df_list:　読み込まれたログデータのDataFrameリスト
    :param file_list:　各DataFrameに対応するファイルパスのリスト
    :return:　クレンジング・統合されたログデータ
    """

    parsed_df_list = []
    logger.info(f'Parsing started')
    for df,file_path in zip(df_list, file_list):
        file_resolved = file_path.resolve()

        try:
            parsed_df = parse_one(df, file_resolved)
        except (ValueError, TypeError, KeyError) as e:
            logger.exception(f'Failed to parse file: {file_resolved}')
            continue

        if parsed_df.empty:
            logger.error(f'No data found from file after parsing: {file_resolved}')
            continue
        parsed_df_list.append(parsed_df)

    if not parsed_df_list:
        logger.error(f'All files are empty or empty after parsing')
        raise RuntimeError(f'All files are empty or empty after parsing')

    logger.info('All Parsing completed')
    return pd.concat(parsed_df_list, ignore_index=True)


def parse_one(df : pd.DataFrame, file : Path) -> pd.DataFrame:
    """
    単一ログファイルのデータをクレンジングする関数

    必須列の存在確認、欠損したデートの除外、日時形式変換、重複データ削除などの前処理を行う。
    不正なデータ形式や必須項目不足の場合は例外を検知し、上位処理に通知する。

    :param df: 1つのログファイルから読み込まれたDataFrame
    :param file: 対象ログファイルのパス
    :return:　クレンジングされたログデータ
    """

    if df.empty:
        return df
    file_resolved = file.resolve()
    # 解析・出力で参照する必須列
    column_list = ['server_name', 'timestamp', 'level', 'cpu_usage', 'memory_usage', 'message']
    if not all(col in df.columns for col in column_list):
        logger.error(f'Missing columns in file: {file_resolved}')
        raise KeyError(f'Missing columns in file: {file_resolved}')

    logger.info(f'Parsing file: {file_resolved}')
    try:
        df = df.dropna(subset=['server_name', 'timestamp', 'message'])

        df['timestamp'] = pd.to_datetime(df['timestamp'], format='%Y-%m-%d %H:%M:%S', errors='coerce')
        df = df.dropna(subset=['timestamp'])

        df = df.drop_duplicates()
    except (ValueError, TypeError, KeyError) as e:
        logger.error(f'Data is not valid: {file_resolved}: {e}')
        raise

    logger.info(f'Parsing completed: {file_resolved}')
    return df


#ここからはテストです
if __name__ == '__main__':
    setup_logging(level=logging.DEBUG)
    test_data = {
        'server_name': ['s1', 's2', None],
        'timestamp': [
            '2025-01-01 07:50:00',
            '45-55-2000 66:20:00',
            '2025-01-01 11:00:00'
        ],
        'level': ['INFO', 'ERROR', 'WARNING'],
        'cpu_usage': [30, 50, 60],
        'memory_usage': [40, 70, 80],
        'message': ['これはメッセージです', '这是一条消息', 'This is a message']
    }
    df_test = pd.DataFrame(test_data)

    parsed_data = parse_one(df_test, Path('fake_path.csv'))
    print(parsed_data)