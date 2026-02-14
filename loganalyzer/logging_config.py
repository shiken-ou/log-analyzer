import logging
from pathlib import Path
from typing import Union
from logging.handlers import RotatingFileHandler


_setup_flag = False

def setup_logging(log_dir : Union[Path, None] = None, level = logging.INFO):
    """
    ログ出力設定を初期化する関数

    ファイルログおよびコンソールログの出力設定を行い、
    指定されたディレクトリにログファイルを生成する。
    多重初期化を防ぐため、一度のみ実行される仕組みになっている。

    :param log_dir:ログファイルの出力先ディレクトリ
    :param level:ログ出力レベル
    :return:なし
    """

    global _setup_flag
    if _setup_flag:
        return

    default_log_dir = Path(__file__).parent.parent / 'logs'
    if log_dir:
        log_dir = Path(log_dir)
    else:
        log_dir = default_log_dir
    log_dir.mkdir(parents=True, exist_ok=True)

    rotating_handler = RotatingFileHandler(
        filename= log_dir / 'log.log',
        mode='a',
        maxBytes= 1024 * 1024 * 1024,
        backupCount= 10
    )
    formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(name)s | %(message)s')
    rotating_handler.setFormatter(formatter)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    logger = logging.getLogger()
    logger.addHandler(rotating_handler)
    logger.addHandler(stream_handler)
    logger.setLevel(level)

    _setup_flag = True