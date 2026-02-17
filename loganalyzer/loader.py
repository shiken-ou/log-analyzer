"""
指定ディレクトリを再帰的に読み込み、CSV/JSON のログファイルを DataFrame のリストとして読み込む。
"""
import logging
from pathlib import Path
import pandas as pd
from loganalyzer.logging_config import setup_logging

logger = logging.getLogger(__name__)

def load_logs_from_dir(data_dir : Path) -> (list[pd.DataFrame], list[Path]):
    """
    指定ディレクトリのログファイルを読み込む関数

    対象となるCSVおよびJSON形式のログファイルを再帰的に検索し、
    ファイルをDataFrame形式で読み込む。

    読み込みに成功したファイルとDataFrameのリストを返却する。
    不正なファイル形式や読み込み失敗時は、ログに記録した上で処理をスキップする。

    :param data_dir:　ログデータが格納されているディレクトリのパス
    :return:　読み込んだログデータのDataFrameリストと、ファイルパスのリスト。
    """

    df_list: list[pd.DataFrame] = []
    file_list: list[Path] = []
    data_dir_resolved = data_dir.resolve()
    logger.info(f'Loading files from {data_dir_resolved}')

    for file in data_dir.rglob('*'):
        file_resolved = file.resolve()

        if not file.is_file():
            logger.warning(f'This is not a file: {file_resolved}')
            continue
        if not file.suffix in ['.csv', '.json']:
            logger.warning(f'File does not have a .csv or .json extension: {file_resolved}')
            continue

        df = None
        if file.suffix.lower() == '.csv':
            try:
                logger.info(f'Loading csv file: {file_resolved}')
                df = pd.read_csv(file)
            except Exception as e:
                logger.error(f'Failed to read {file_resolved}: {e}')

        elif file.suffix.lower() == '.json':
            try:
                logger.info(f'Loading json file: {file_resolved}')
                df = pd.read_json(file)
            except Exception as e:
                logger.error(f'Failed to read {file_resolved}: {e}')

        # 読み込み成功時のみリストに追加（None を渡さない）
        if df is not None:
            df_list.append(df)
            file_list.append(file)

    if not df_list:
        logger.exception(f'No csv or json file in directory: {data_dir_resolved}')
        raise FileNotFoundError(f'No csv or json file in directory: {data_dir_resolved}')

    logger.info(f'Loaded {len(df_list)} files from {data_dir_resolved}')
    return df_list, file_list

#ここからはテストです
if __name__ == '__main__':
    setup_logging(level= logging.DEBUG)
    dfs, files = load_logs_from_dir(Path(__file__).parent.parent / 'data' / 'sample_logs' )
    print(dfs)
    print(files)