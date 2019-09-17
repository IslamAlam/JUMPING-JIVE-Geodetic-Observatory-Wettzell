from datetime import datetime
import pandas as pd

from dateutil.relativedelta import relativedelta
from datetime import date, time

import json


url = "https://ivscc.gsfc.nasa.gov/sessions/2019/"
df = pd.read_html(url, header=0, parse_dates=True)[0] #, match='.+', flavor=None, header=None, index_col=None, skiprows=None, attrs=None, parse_dates=False, thousands=', ', encoding=None, decimal='.', converters=None, na_values=None, keep_default_na=True, displayed_only=True
df = df.dropna(how='all', subset=['Code'])
new_dates, new_times = zip(*[(datetime.strptime(d, '%Y-%m-%d %H:%M').date(), datetime.strptime(d, '%Y-%m-%d %H:%M').time()) for d in  df['Start']]) #datetime.datetime.strptime(d, '%Y-%m-%d %H:%M')
df = df.assign(start_date=new_dates, start_time=new_times)
Stations = df["Stations"].str.split("\s\s")
df["Split_Stations"] = Stations
df.head()
today = pd.datetime.today().date()

today_next_year = today + relativedelta(days=+0)

df_today = df.loc[df['start_date'].between(today, today_next_year)]
df_today.head()
json_str = df_today.to_json(orient='records')

from sqlalchemy import create_engine
engine = create_engine('postgresql://zabbix:zabbix@localhost:8080/postgres-server')
df.to_sql('table_name', engine)