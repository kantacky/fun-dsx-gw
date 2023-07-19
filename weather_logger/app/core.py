from config import POSTGRES_DB
import datetime
from db import Database
import numpy as np
import pandas as pd

def core():
    d = {
        "北": 0,
        "北北東": 22.5,
        "北東": 45,
        "東北東": 67.5,
        "東": 90,
        "東南東": 112.5,
        "南東": 135,
        "南南東": 157.5,
        "南": 180,
        "南南西": 202.5,
        "南西": 225,
        "西南西": 247.5,
        "西": 270,
        "西北西": 292.5,
        "北西": 315,
        "北北西": 337.5,
    }

    # 降水量
    df1 = pd.read_csv('https://www.data.jma.go.jp/obd/stats/data/mdrr/pre_rct/alltable/pre1h00_rct.csv', encoding='shift_jis')
    df1 = df1.drop(['都道府県', '地点', '国際地点番号', '今日の最大値(mm)', '今日の最大値の品質情報', '今日の最大値起時（時）(まで)', '今日の最大値起時（分）(まで)', '今日の最大値起時(まで)の品質情報', '極値更新', '10年未満での極値更新', '昨日までの観測史上1位の値(mm)', '昨日までの観測史上1位の値の品質情報', '昨日までの観測史上1位の値の年', '昨日までの観測史上1位の値の月', '昨日までの観測史上1位の値の日', '昨日までの7月の1位の値(mm)', '昨日までの7月の1位の値の品質情報', '昨日までの7月の1位の値の年', '昨日までの7月の1位の値の月', '昨日までの7月の1位の値の日', '統計開始年'], axis=1)
    df1 = df1.dropna(subset=['現在時刻(年)', '現在時刻(月)', '現在時刻(日)', '現在時刻(時)', '現在時刻(分)'])
    df1 = df1.replace(np.nan, None)
    df1.reset_index()

    df1['現在時刻(年)'] = [datetime.datetime(int(row['現在時刻(年)']), int(row['現在時刻(月)']), int(row['現在時刻(日)']), int(row['現在時刻(時)']), int(row['現在時刻(分)']), 0, 0, tzinfo=datetime.timezone(datetime.timedelta(hours=9))) for index, row in df1.iterrows()]
    df1 = df1.drop(['現在時刻(月)', '現在時刻(日)', '現在時刻(時)', '現在時刻(分)'], axis=1)
    df1 = df1.rename(columns={'現在時刻(年)': '現在時刻'})

    df1 = df1.rename(columns={
        '観測所番号': 'observatory_id',
        '現在時刻': 'timestamp',
        '現在値(mm)': 'value_mm',
        '現在値の品質情報': 'value_quality'
    })

    df1['observatory_id'] = df1['observatory_id'].astype(int)
    df1['value_mm'] = df1['value_mm'].astype(float)
    df1['value_quality'] = df1['value_quality'].astype(int)


    # 最大風速
    df2 = pd.read_csv('https://www.data.jma.go.jp/obd/stats/data/mdrr/wind_rct/alltable/mxwsp00_rct.csv', encoding='shift_jis')
    df2 = df2.drop(['都道府県', '地点', '国際地点番号', '極値更新', '10年未満での極値更新', '昨日までの観測史上1位の値(m/s)', '昨日までの観測史上1位の値の品質情報', '昨日までの観測史上1位の値観測時の風向', '昨日までの観測史上1位の値観測時の風向の品質情報', '昨日までの観測史上1位の値観測時の年', '昨日までの観測史上1位の値観測時の月', '昨日までの観測史上1位の値観測時の日', '昨日までの7月の1位の値(m/s)', '昨日までの7月の1位の値の品質情報', '昨日までの7月の1位の値観測時の風向', '昨日までの7月の1位の値観測時の風向の品質情報', '昨日までの7月の1位の値観測時の年', '昨日までの7月の1位の値観測時の月', '昨日までの7月の1位の値観測時の日', '統計開始年'], axis=1)
    df2 = df2.dropna(subset=['現在時刻(年)', '現在時刻(月)', '現在時刻(日)', '現在時刻(時)', '現在時刻(分)', '今日の最大値起時（時）', '今日の最大値起時（分）'])
    df2 = df2.replace(np.nan, None)
    df2.reset_index()

    df2['今日の最大値起時（時）'] = [datetime.datetime(int(row['現在時刻(年)']), int(row['現在時刻(月)']), int(row['現在時刻(日)']), int(row['今日の最大値起時（時）']), int(row['今日の最大値起時（分）']), 0, 0, tzinfo=datetime.timezone(datetime.timedelta(hours=9))) for index, row in df2.iterrows()]
    df2 = df2.drop(['今日の最大値起時（分）'], axis=1)
    df2 = df2.rename(columns={'今日の最大値起時（時）': '今日の最大値起時'})

    df2['現在時刻(年)'] = [datetime.datetime(int(row['現在時刻(年)']), int(row['現在時刻(月)']), int(row['現在時刻(日)']), int(row['現在時刻(時)']), int(row['現在時刻(分)']), 0, 0, tzinfo=datetime.timezone(datetime.timedelta(hours=9))) for index, row in df2.iterrows()]
    df2 = df2.drop(['現在時刻(月)', '現在時刻(日)', '現在時刻(時)', '現在時刻(分)'], axis=1)
    df2 = df2.rename(columns={'現在時刻(年)': '現在時刻'})

    df2 = df2.rename(columns={
        '観測所番号': 'observatory_id',
        '現在時刻': 'timestamp',
        '今日の最大値(m/s)': 'max_today_mps',
        '今日の最大値の品質情報': 'max_today_value_quality',
        '今日の最大値観測時の風向': 'max_today_direction_degree',
        '今日の最大値観測時の風向の品質情報': 'max_today_direction_value_quality',
        '今日の最大値起時': 'max_today_timestamp',
        '今日の最大値起時の品質情報': 'max_today_timestamp_value_quality'
    })

    df2['max_today_direction_degree'] = pd.DataFrame([d[i] for i in df2['max_today_direction_degree'].values])

    df2['observatory_id'] = df2['observatory_id'].astype(int)
    df2['max_today_mps'] = df2['max_today_mps'].astype(float)
    df2['max_today_value_quality'] = df2['max_today_value_quality'].astype(int)
    df2['max_today_direction_degree'] = df2['max_today_direction_degree'].astype(float)
    df2['max_today_direction_value_quality'] = df2['max_today_direction_value_quality'].astype(int)
    df2['max_today_timestamp_value_quality'] = df2['max_today_timestamp_value_quality'].astype(int)


    # 最大瞬間風速
    df3 = pd.read_csv('https://www.data.jma.go.jp/obd/stats/data/mdrr/wind_rct/alltable/gust00_rct.csv', encoding='shift_jis')
    df3 = df3.drop(['都道府県', '地点', '国際地点番号', '極値更新', '10年未満での極値更新', '昨日までの観測史上1位の値(m/s)', '昨日までの観測史上1位の値の品質情報', '昨日までの観測史上1位の値観測時の風向', '昨日までの観測史上1位の値観測時の風向の品質情報', '昨日までの観測史上1位の値観測時の年', '昨日までの観測史上1位の値観測時の月', '昨日までの観測史上1位の値観測時の日', '昨日までの7月の1位の値（m/s）', '昨日までの7月の1位の値の品質情報', '昨日までの7月の1位の値観測時の風向', '昨日までの7月の1位の値観測時の風向の品質情報', '昨日までの7月の1位の値観測時の年', '昨日までの7月の1位の値観測時の月', '昨日までの7月の1位の値観測時の日', '統計開始年'], axis=1)
    df3 = df3.dropna(subset=['現在時刻(年)', '現在時刻(月)', '現在時刻(日)', '現在時刻(時)', '現在時刻(分)', '今日の最大値起時（時）', '今日の最大値起時（分）'])
    df3 = df3.replace(np.nan, None)
    df3.reset_index()

    df3['今日の最大値起時（時）'] = [datetime.datetime(int(row['現在時刻(年)']), int(row['現在時刻(月)']), int(row['現在時刻(日)']), int(row['今日の最大値起時（時）']), int(row['今日の最大値起時（分）']), 0, 0, tzinfo=datetime.timezone(datetime.timedelta(hours=9))) for index, row in df3.iterrows()]
    df3 = df3.drop(['今日の最大値起時（分）'], axis=1)
    df3 = df3.rename(columns={'今日の最大値起時（時）': '今日の最大値起時'})

    df3['現在時刻(年)'] = [datetime.datetime(int(row['現在時刻(年)']), int(row['現在時刻(月)']), int(row['現在時刻(日)']), int(row['現在時刻(時)']), int(row['現在時刻(分)']), 0, 0, tzinfo=datetime.timezone(datetime.timedelta(hours=9))) for index, row in df3.iterrows()]
    df3 = df3.drop(['現在時刻(月)', '現在時刻(日)', '現在時刻(時)', '現在時刻(分)'], axis=1)
    df3 = df3.rename(columns={'現在時刻(年)': '現在時刻'})

    df3 = df3.rename(columns={
        '観測所番号': 'observatory_id',
        '現在時刻': 'timestamp',
        '今日の最大値(m/s)': 'max_today_mps',
        '今日の最大値の品質情報': 'max_today_value_quality',
        '今日の最大値観測時の風向': 'max_today_direction_degree',
        '今日の最大値観測時の風向の品質情報': 'max_today_direction_value_quality',
        '今日の最大値起時': 'max_today_timestamp',
        '今日の最大値起時の品質情報': 'max_today_timestamp_value_quality'
    })

    df3['max_today_direction_degree'] = pd.DataFrame([d[i] for i in df3['max_today_direction_degree'].values])

    df3['observatory_id'] = df3['observatory_id'].astype(int)
    df3['max_today_mps'] = df3['max_today_mps'].astype(float)
    df3['max_today_value_quality'] = df3['max_today_value_quality'].astype(int)
    df3['max_today_direction_degree'] = df3['max_today_direction_degree'].astype(float)
    df3['max_today_direction_value_quality'] = df3['max_today_direction_value_quality'].astype(int)
    df3['max_today_timestamp_value_quality'] = df3['max_today_timestamp_value_quality'].astype(int)


    # 最高気温
    df4 = pd.read_csv('https://www.data.jma.go.jp/obd/stats/data/mdrr/tem_rct/alltable/mxtemsadext00_rct.csv', encoding='shift_jis')
    df4 = df4.drop(['都道府県', '地点', '国際地点番号', '該当旬（月）', '該当旬（旬）', '今年最高', '極値更新', '10年未満での極値更新', '今年の最高気温（℃)（昨日まで）', '今年の最高気温（昨日まで）の品質情報', '今年の最高気温（昨日まで）を観測した起日（年）', '今年の最高気温（昨日まで）を観測した起日（月）', '今年の最高気温（昨日まで）を観測した起日（日）', '昨日までの観測史上1位の値（℃）', '昨日までの観測史上1位の値の品質情報', '昨日までの観測史上1位の値を観測した起日（年）', '昨日までの観測史上1位の値を観測した起日（月）', '昨日までの観測史上1位の値を観測した起日（日）', '昨日までの7月の1位の値', '昨日までの7月の1位の値の品質情報', '昨日までの7月の1位の値の起日（年）', '昨日までの7月の1位の値の起日（月）', '昨日までの7月の1位の値の起日（日）', '統計開始年'], axis=1)
    df4 = df4.dropna(subset=['現在時刻(年)', '現在時刻(月)', '現在時刻(日)', '現在時刻(時)', '現在時刻(分)', '今日の最高気温起時（時）', '今日の最高気温起時（分）'])
    df4 = df4.replace(np.nan, None)
    df4.reset_index()

    df4['今日の最高気温起時（時）'] = [datetime.datetime(int(row['現在時刻(年)']), int(row['現在時刻(月)']), int(row['現在時刻(日)']), int(row['今日の最高気温起時（時）']), int(row['今日の最高気温起時（分）']), 0, 0, tzinfo=datetime.timezone(datetime.timedelta(hours=9))) for index, row in df4.iterrows()]
    df4 = df4.drop(['今日の最高気温起時（分）'], axis=1)
    df4 = df4.rename(columns={'今日の最高気温起時（時）': '今日の最高気温起時'})

    df4['現在時刻(年)'] = [datetime.datetime(int(row['現在時刻(年)']), int(row['現在時刻(月)']), int(row['現在時刻(日)']), int(row['現在時刻(時)']), int(row['現在時刻(分)']), 0, 0, tzinfo=datetime.timezone(datetime.timedelta(hours=9))) for index, row in df4.iterrows()]
    df4 = df4.drop(['現在時刻(月)', '現在時刻(日)', '現在時刻(時)', '現在時刻(分)'], axis=1)
    df4 = df4.rename(columns={'現在時刻(年)': '現在時刻'})

    df4 = df4.rename(columns={
        '観測所番号': 'observatory_id',
        '現在時刻': 'timestamp',
        '今日の最高気温(℃)': 'max_today_degree_c',
        '今日の最高気温の品質情報': 'max_today_value_quality',
        '今日の最高気温起時': 'max_today_timestamp',
        '今日の最高気温起時の品質情報': 'max_today_timestamp_value_quality',
        '平年差（℃）': 'diff_normal_degree_c',
        '前日差（℃）': 'diff_yesterday_degree_c'
    })

    df4['observatory_id'] = df4['observatory_id'].astype(int)
    df4['max_today_degree_c'] = df4['max_today_degree_c'].astype(float)
    df4['max_today_value_quality'] = df4['max_today_value_quality'].astype(int)
    df4['max_today_timestamp_value_quality'] = df4['max_today_timestamp_value_quality'].astype(int)
    df4['diff_normal_degree_c'] = df4['diff_normal_degree_c'].astype(float)
    df4['diff_yesterday_degree_c'] = df4['diff_yesterday_degree_c'].astype(float)


    # 最低気温
    df5 = pd.read_csv('https://www.data.jma.go.jp/obd/stats/data/mdrr/tem_rct/alltable/mntemsadext00_rct.csv', encoding='shift_jis')
    df5 = df5.drop(['都道府県', '地点', '国際地点番号', '該当旬（月）', '該当旬（旬）', '今季最低', '極値更新', '10年未満での極値更新', '今年の最低気温（℃)（昨日まで）', '今年の最低気温（昨日まで）の品質情報', '今年の最低気温（昨日まで）を観測した起日（年）', '今年の最低気温（昨日まで）を観測した起日（月）', '今年の最低気温（昨日まで）を観測した起日（日）', '昨日までの観測史上1位の値（℃）', '昨日までの観測史上1位の値の品質情報', '昨日までの観測史上1位の値を観測した起日（年）', '昨日までの観測史上1位の値を観測した起日（月）', '昨日までの観測史上1位の値を観測した起日（日）', '昨日までの7月の1位の値', '昨日までの7月の1位の値の品質情報', '昨日までの7月の1位の値の起日（年）', '昨日までの7月の1位の値の起日（月）', '昨日までの7月の1位の値の起日（日）', '統計開始年'], axis=1)
    df5 = df5.dropna(subset=['現在時刻(年)', '現在時刻(月)', '現在時刻(日)', '現在時刻(時)', '現在時刻(分)', '今日の最低気温起時（時）', '今日の最低気温起時（分）'])
    df5 = df5.replace(np.nan, None)
    df5.reset_index()

    df5['今日の最低気温起時（時）'] = [datetime.datetime(int(row['現在時刻(年)']), int(row['現在時刻(月)']), int(row['現在時刻(日)']), int(row['今日の最低気温起時（時）']), int(row['今日の最低気温起時（分）']), 0, 0, tzinfo=datetime.timezone(datetime.timedelta(hours=9))) for index, row in df5.iterrows()]
    df5 = df5.drop(['今日の最低気温起時（分）'], axis=1)
    df5 = df5.rename(columns={'今日の最低気温起時（時）': '今日の最低気温起時'})

    df5['現在時刻(年)'] = [datetime.datetime(int(row['現在時刻(年)']), int(row['現在時刻(月)']), int(row['現在時刻(日)']), int(row['現在時刻(時)']), int(row['現在時刻(分)']), 0, 0, tzinfo=datetime.timezone(datetime.timedelta(hours=9))) for index, row in df5.iterrows()]
    df5 = df5.drop(['現在時刻(月)', '現在時刻(日)', '現在時刻(時)', '現在時刻(分)'], axis=1)
    df5 = df5.rename(columns={'現在時刻(年)': '現在時刻'})

    df5 = df5.rename(columns={
        '観測所番号': 'observatory_id',
        '現在時刻': 'timestamp',
        '今日の最低気温(℃)': 'min_today_degree_c',
        '今日の最低気温の品質情報': 'min_today_value_quality',
        '今日の最低気温起時': 'min_today_timestamp',
        '今日の最低気温起時の品質情報': 'min_today_timestamp_value_quality',
        '平年差（℃）': 'diff_normal_degree_c',
        '前日差（℃）': 'diff_yesterday_degree_c'
    })

    df5['observatory_id'] = df5['observatory_id'].astype(int)
    df5['min_today_degree_c'] = df5['min_today_degree_c'].astype(float)
    df5['min_today_value_quality'] = df5['min_today_value_quality'].astype(int)
    df5['min_today_timestamp_value_quality'] = df5['min_today_timestamp_value_quality'].astype(int)
    df5['diff_normal_degree_c'] = df5['diff_normal_degree_c'].astype(float)
    df5['diff_yesterday_degree_c'] = df5['diff_yesterday_degree_c'].astype(float)


    db = Database(database_name=POSTGRES_DB)

    with db.get_connection() as conn:
        with conn.cursor() as cur:
            with cur.copy(f"COPY weather.precipitation ({','.join(df1.columns)}) FROM STDIN") as copy:
                for row in df1.values:
                    copy.write_row(row)

            with cur.copy(f"COPY weather.max_wind_speed ({','.join(df2.columns)}) FROM STDIN") as copy:
                for row in df2.values:
                    copy.write_row(row)

            with cur.copy(f"COPY weather.max_instantaneous_wind_speed ({','.join(df3.columns)}) FROM STDIN") as copy:
                for row in df3.values:
                    copy.write_row(row)
            
            with cur.copy(f"COPY weather.max_temperature ({','.join(df4.columns)}) FROM STDIN") as copy:
                for row in df4.values:
                    copy.write_row(row)

            with cur.copy(f"COPY weather.min_temperature ({','.join(df5.columns)}) FROM STDIN") as copy:
                for row in df5.values:
                    copy.write_row(row)
        conn.commit()
