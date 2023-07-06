from config import ODPT_ACCESS_TOKEN
from config import POSTGRES_DB
from config import arrival_column_drop_list, departure_column_drop_list
from config import arrival_column_rename_list, departure_column_rename_list
from datetime import datetime
from db import Database
import numpy as np
import pandas as pd

def core():
    # Get pandas dataframe from json
    df_departure = pd.read_json(f"https://api.odpt.org/api/v4/odpt:FlightInformationDeparture?odpt:operator=odpt.Operator:JAL&acl:consumerKey={ODPT_ACCESS_TOKEN}")
    df_arrival = pd.read_json(f"https://api.odpt.org/api/v4/odpt:FlightInformationArrival?odpt:operator=odpt.Operator:JAL&acl:consumerKey={ODPT_ACCESS_TOKEN}")

    # Drop unnecessary columns
    df_departure = df_departure.drop(departure_column_drop_list, axis=1)
    df_arrival = df_arrival.drop(arrival_column_drop_list, axis=1)

    # Rename columns
    df_departure = df_departure.rename(departure_column_rename_list, axis=1)
    df_arrival = df_arrival.rename(arrival_column_rename_list, axis=1)

    # Format data
    df_departure['id'] = pd.Series( (str(v).replace('urn:uuid:', '') for v in df_departure['id'] if v and str(v) != 'nan') )
    df_departure['flight_number'] = pd.Series( (v[0] for v in df_departure['flight_number'] if v and str(v) != 'nan') )
    df_departure['departure_airport'] = pd.Series( (str(v).replace('odpt.Airport:', '') for v in df_departure['departure_airport'] if v and str(v) != 'nan') )
    df_departure['destination_airport'] = pd.Series( (str(v).replace('odpt.Airport:', '') for v in df_departure['destination_airport'] if v and str(v) != 'nan') )
    df_departure['flight_status'] = pd.Series( (str(v).replace('odpt.FlightStatus:', '') for v in df_departure['flight_status'] if v and str(v) != 'nan') )
    df_departure['actual_departure_time'] = pd.Series( (f"{str(datetime.today()).split(' ')[0]}T{v}:00+09:00" for v in df_departure['actual_departure_time'] if v and str(v) != 'nan') )
    df_departure['scheduled_departure_time'] = pd.Series( (f"{str(datetime.today()).split(' ')[0]}T{v}:00+09:00" for v in df_departure['scheduled_departure_time'] if v and str(v) != 'nan') )
    df_departure['estimated_departure_time'] = pd.Series( (f"{str(datetime.today()).split(' ')[0]}T{v}:00+09:00" for v in df_departure['estimated_departure_time'] if v and str(v) != 'nan') )
    df_arrival['id'] = pd.Series( (str(v).replace('urn:uuid:', '') for v in df_arrival['id'] if v and str(v) != 'nan') )
    df_arrival['flight_number'] = pd.Series( (v[0] for v in df_arrival['flight_number'] if v and str(v) != 'nan') )
    df_arrival['origin_airport'] = pd.Series( (str(v).replace('odpt.Airport:', '') for v in df_arrival['origin_airport'] if v and str(v) != 'nan') )
    df_arrival['arrival_airport'] = pd.Series( (str(v).replace('odpt.Airport:', '') for v in df_arrival['arrival_airport'] if v and str(v) != 'nan') )
    df_arrival['flight_status'] = pd.Series( (str(v).replace('odpt.FlightStatus:', '') for v in df_arrival['flight_status'] if v and str(v) != 'nan') )
    df_arrival['actual_arrival_time'] = pd.Series( (f"{str(datetime.today()).split(' ')[0]}T{v}:00+09:00" for v in df_arrival['actual_arrival_time'] if v and str(v) != 'nan') )
    df_arrival['scheduled_arrival_time'] = pd.Series( (f"{str(datetime.today()).split(' ')[0]}T{v}:00+09:00" for v in df_arrival['scheduled_arrival_time'] if v and str(v) != 'nan') )
    df_arrival['estimated_arrival_time'] = pd.Series( (f"{str(datetime.today()).split(' ')[0]}T{v}:00+09:00" for v in df_arrival['estimated_arrival_time'] if v and str(v) != 'nan') )

    df_departure = df_departure.replace(np.nan, None)
    df_arrival = df_arrival.replace(np.nan, None)

    db = Database(database_name=POSTGRES_DB)

    with db.get_connection() as conn:
        with conn.cursor() as cur:
            with cur.copy(f"COPY jal_op.departure ({','.join(df_departure.columns)}) FROM STDIN") as copy:
                for row in df_departure.values:
                    copy.write_row(row)

            with cur.copy(f"COPY jal_op.arrival ({','.join(df_arrival.columns)}) FROM STDIN") as copy:
                for row in df_arrival.values:
                    copy.write_row(row)
        conn.commit()
