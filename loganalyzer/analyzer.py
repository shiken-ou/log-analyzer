import pandas as pd
import logging
from loganalyzer.logging_config import setup_logging

logger = logging.getLogger(__name__)

def analyze_df(df: pd.DataFrame) -> pd.DataFrame:
    """
    ログデータを分析し、サーバー別・日別の集計結果を作成する関数

    timestamp列から日付（date）列を生成し、ログレベル別件数を集計する
    CPU / メモリ使用率の平均値を算出する
    集計結果を結合して1つのDataFrameにまとめる

    :param df:　パース済みのログデータ
    :return:　分析・集計後のデータ
    """

    logger.info(f'Analysis started')
    try:
        logger.debug('Processing data column')
        df['date'] = df['timestamp'].dt.date

        logger.debug('Grouping by name, date, level')
        leveled_df = df.groupby(['server_name', 'date', 'level']).size().unstack(fill_value=0)
        usage_age_daily = df.groupby(['server_name','date']).agg(
            cpu_avg = ('cpu_usage', 'mean'),
            memory_avg = ('memory_usage', 'mean')
        )

        logger.debug('Merging data')
        df_analyzed = pd.merge(
            leveled_df.reset_index(),
            usage_age_daily.reset_index(),
            on=['server_name', 'date'],
            how='outer')

    except (ValueError, TypeError, KeyError) as e:
        logger.exception(f'Analysis failed: {e}')
        raise


    logger.info(f'Analysis completed')
    return df_analyzed


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

    print(analyze_df(data))

