import logging
from pathlib import Path
import pandas as pd
from loganalyzer.logging_config import setup_logging

logger = logging.getLogger(__name__)

def load_logs_from_dir(data_dir : Path) -> (list[pd.DataFrame], list[Path]):

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

        df_list.append(df)
        file_list.append(file)

    if not df_list:
        logger.exception(f'No csv or json file in directory: {data_dir_resolved}')
        raise FileNotFoundError(f'No csv or json file in directory: {data_dir_resolved}')

    logger.info(f'Loaded {len(df_list)} files from {data_dir_resolved}')
    return df_list, file_list


if __name__ == '__main__':
    setup_logging(level= logging.DEBUG)
    dfs, files = load_logs_from_dir(Path(__file__).parent.parent / 'data' / 'sample_logs' )
    print(dfs)
    print(files)