#!/user/bin/python
import os 
dir_path = os.path.dirname(os.path.realpath(__file__))
print(dir_path)

import time
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
df["Stations_Codes"] = Stations
df.head()
today = pd.datetime.today().date()

today_next_year = today + relativedelta(days=+0)

df_today = df.loc[df['start_date'].between(today + relativedelta(days=-3), today_next_year)]
df_today.head()
#json_str = df_today.to_json(orient='records')
header = ["Name", "Code", "start_date", "start_time", "Dur", "DOY", "Stations_Codes", "DB Code","Ops Center", "Correlator", "Analysis"]
df_today.to_csv(dir_path + "/" +'sessions.csv', columns = header)

#from sqlalchemy import create_engine
#engine = create_engine('postgresql://zabbix:zabbix@localhost:8080/postgres-server')
#df.to_sql('table_name', engine)
#SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')



# https://discourse.nodered.org/t/from-python-script-to-node-red/1352/5