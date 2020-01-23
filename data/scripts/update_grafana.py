# ! pip install grafana-api

import os 
dir_path = os.getcwd() #os.path.dirname(os.path.realpath(__file__))
print(dir_path)

import time
from datetime import datetime
import pandas as pd

from dateutil.relativedelta import relativedelta
from datetime import date, time, timedelta

import json

from grafana_api.grafana_face import GrafanaFace

grafana_api = GrafanaFace(auth='eyJrIjoibDZvZGdzN3RFUDlOc0JQdnNSN0RmTWtnU3hWaWdJM1giLCJuIjoicHl0aG9uIiwiaWQiOjF9', host='138.246.233.65:3000')
current_time = datetime.now() # - relativedelta(days=1, hours=4)
url = "https://ivscc.gsfc.nasa.gov/sessions/" + str(date.today().year) + "/"


def add_datetime(x):
  return datetime.combine(x["start_date"], x["start_time"])

def calc_end_schedule(x):
  hours, minutes = map(int, x["Dur"].split(':'))
  duration = timedelta(hours=hours, minutes=minutes)
  return x["start_schedule"] + duration

def session_to_datafram(session_url):
  session_df = pd.read_html(session_url, header=0, parse_dates=True)[0] #, match='.+', flavor=None, header=None, index_col=None, skiprows=None, attrs=None, parse_dates=False, thousands=', ', encoding=None, decimal='.', converters=None, na_values=None, keep_default_na=True, displayed_only=True
  session_df = session_df.dropna(how='all', subset=['Code'])
  new_dates, new_times = zip(*[(datetime.strptime(d, '%Y-%m-%d %H:%M').date(), datetime.strptime(d, '%Y-%m-%d %H:%M').time()) for d in  session_df['Start']]) #datetime.datetime.strptime(d, '%Y-%m-%d %H:%M')
  session_df = session_df.assign(start_date=new_dates, start_time=new_times)
  Stations = session_df["Stations"].str.split("\s\s")
  session_df["Stations_Codes"] = Stations
  # Create row for start_schedule
  session_df["start_schedule"] = session_df.apply(add_datetime, axis=1) #passes a Series object, row-wise
  session_df["end_schedule"] = session_df.apply(calc_end_schedule, axis=1) #passes a Series object, row-wise

  return session_df[['Name','Code','start_schedule','end_schedule', 'Stations_Codes','DB Code', 'Ops Center', 'Correlator', 'Status', 'Analysis']]

def session_at_time(session_df, current_time):
  return session_df.loc[(session_df['start_schedule'] <=  current_time) & (session_df['end_schedule'] >= current_time )]

def telescope_in_session(current_session_df, telescope_name):
  if any(telescope_name in s for s in current_session_df["Stations_Codes"].values.tolist()):
    print(telescope_name + " is in the session list")
    telescope_participation = True
  else:
    print(telescope_name + " is not in the session list")
    telescope_participation = False
  return telescope_participation


final_session_df = session_to_datafram(url)
current_session_df = session_at_time(final_session_df, current_time)

#json_str = df_today.to_json(orient='records')
header = ['Name','Code','start_schedule','end_schedule', 'Stations_Codes','DB Code', 'Ops Center', 'Correlator', 'Status', 'Analysis']
current_session_df.to_csv(dir_path + "/" +'sessions.csv', columns = header)
current_session_df

# WETTZ13S (Ws)
WETTZ13S = telescope_in_session(current_session_df, "Ws")

# WETTZ13N (Wn)
WETTZ13N = telescope_in_session(current_session_df, "Wn")

# WETTZELL (Wz)
WETTZELL = telescope_in_session(current_session_df, "Wz")

# Change here imp to have new col for star_sch + Dur 
current_session_df


rawQwery_template = \
"""
SELECT 
  h.name AS "station_id" ,
  h.available AS "triggers", 
  i.location_lat AS "lat", 
  i.location_lon AS "lon"
FROM host_inventory AS i, hosts AS h
WHERE 
  i.hostid=h.hostid
  AND i.location_lat!='' AND i.location_lon!=''
  AND ( 
  h.name LIKE '%WETTZELL%'
  OR h.name LIKE '%WETTZ13S%' 
  OR h.name LIKE '%WETTZ13N%'
  )
"""


def de_activate_telescope(rawQwery_template,telescope_active, telescope_name):
  if telescope_active == True:
    print(telescope_name +" is in the currnet session")
    return rawQwery_template.replace("NULL_" + telescope_name, telescope_name)
    # grafana_table_dashboard['dashboard']['panels'][0]['targets'][0]['hide'] = False
  else:
    print(telescope_name + " is not in the currnet session")
    return rawQwery_template.replace(telescope_name, "NULL_" + telescope_name)


rawQwery = de_activate_telescope(rawQwery_template, WETTZELL, "WETTZELL")
rawQwery = de_activate_telescope(rawQwery, WETTZ13S, "WETTZ13S")
rawQwery = de_activate_telescope(rawQwery, WETTZ13N, "WETTZ13N")


# Create or update a dashboard
grafana_table_dashboard_json = \
{'dashboard': {'annotations': {'list': [{'builtIn': 1,
     'datasource': '-- Grafana --',
     'enable': True,
     'hide': True,
     'iconColor': 'rgba(0, 211, 255, 1)',
     'name': 'Annotations & Alerts',
     'type': 'dashboard'}]},
  'editable': True,
  'gnetId': None,
  'graphTooltip': 0,
  'id': 6,
  'links': [],
  'panels': [{'columns': [],
    'datasource': 'PostgreSQL',
    'fontSize': '100%',
    'gridPos': {'h': 9, 'w': 12, 'x': 0, 'y': 0},
    'id': 2,
    'links': [],
    'options': {},
    'pageSize': None,
    'scroll': True,
    'showHeader': True,
    'sort': {'col': 0, 'desc': True},
    'styles': [{'alias': 'Time',
      'dateFormat': 'YYYY-MM-DD HH:mm:ss',
      'pattern': 'Time',
      'type': 'date'},
     {'alias': '',
      'colorMode': None,
      'colors': ['rgba(245, 54, 54, 0.9)',
       'rgba(237, 129, 40, 0.89)',
       'rgba(50, 172, 45, 0.97)'],
      'decimals': 2,
      'pattern': '/.*/',
      'thresholds': [],
      'type': 'number',
      'unit': 'short'}],
    'targets': [{'format': 'table',
      'group': [],
      'hide': False,
      'metricColumn': 'none',
      'rawQuery': True,
      'rawSql': 'SELECT \r\n  h.name AS "station_id" , /* LIKE \'D%\'    SUBSTRING(h.name, \'WETTZELL*([0-9]{1,3})\') AS "station_id" */\r\n  h.available AS "triggers", \r\n  i.location_lat AS "lat", \r\n  i.location_lon AS "lon"\r\nFROM host_inventory AS i, hosts AS h\r\nWHERE \r\n  i.hostid=h.hostid AND h.name LIKE \'%WETTZELL%\' /* AND i.location_lon!=\'\'  AND h.name SIMILAR TO \'*.WETTZELL.*\'  */\r\n  \r\n/* GROUP BY "station_id" */',
      'refId': 'A',
      'select': [[{'params': ['value'], 'type': 'column'}]],
      'timeColumn': 'time',
      'where': [{'name': '$__timeFilter', 'params': [], 'type': 'macro'}]}],
    'timeFrom': None,
    'timeShift': None,
    'title': 'Panel Title',
    'transform': 'table',
    'type': 'table'},
   {'circleMaxSize': '50',
    'circleMinSize': '10',
    'colors': ['#56a64b',
     'rgba(151, 170, 179, 0.89)',
     'rgba(116, 153, 255, 0.97)',
     'rgba(255, 200, 89, 0.97)',
     'rgba(255, 160, 89, 0.97)',
     'rgba(233, 118, 89, 0.97)',
     '#e02f44'],
    'datasource': 'PostgreSQL',
    'decimals': 0,
    'esMetric': 'Count',
    'gridPos': {'h': 9, 'w': 12, 'x': 12, 'y': 0},
    'hideEmpty': False,
    'hideZero': False,
    'id': 4,
    'initialZoom': '14',
    'locationData': 'table',
    'mapCenter': 'custom',
    'mapCenterLatitude': '49.145',
    'mapCenterLongitude': '12.89 ',
    'maxDataPoints': 1,
    'mouseWheelZoom': False,
    'options': {},
    'showLegend': False,
    'stickyLabels': False,
    'tableQueryOptions': {'geohashField': 'geohash',
     'labelField': 'station_id',
     'latitudeField': 'lat',
     'longitudeField': 'lon',
     'metricField': 'triggers',
     'queryType': 'coordinates'},
    'targets': [{'format': 'table',
      'group': [],
      'hide': False,
      'metricColumn': 'none',
      'rawQuery': True,
      'rawSql': 'SELECT \r\n  h.name AS "station_id" , /* LIKE \'D%\'    SUBSTRING(h.name, \'WETTZELL*([0-9]{1,3})\') AS "station_id" */\r\n  h.available AS "triggers", \r\n  i.location_lat AS "lat", \r\n  i.location_lon AS "lon"\r\nFROM host_inventory AS i, hosts AS h\r\nWHERE \r\n  i.hostid=h.hostid AND h.name LIKE \'%WETTZELL%\' \r\n  OR h.name LIKE \'%WETTZ13S%\' \r\n  OR h.name LIKE \'%WETTZ13N%\'\r\n  \r\n  /* AND i.location_lon!=\'\'  AND h.name SIMILAR TO \'*.WETTZELL.*\'  */\r\n  \r\n/* GROUP BY "station_id" */\r\n',
      'refId': 'A',
      'select': [[{'params': ['value'], 'type': 'column'}]],
      'timeColumn': 'time',
      'where': [{'name': '$__timeFilter', 'params': [], 'type': 'macro'}]}],
    'thresholds': '0,1,2,3,4,5',
    'timeFrom': None,
    'timeShift': None,
    'title': 'Panel Title',
    'type': 'grafana-worldmap-panel',
    'unitPlural': '',
    'unitSingle': '',
    'valueName': 'current'}],
  'schemaVersion': 18,
  'style': 'dark',
  'tags': ['python_map'],
  'templating': {'list': []},
  'time': {'from': 'now-6h', 'to': 'now'},
  'timepicker': {'refresh_intervals': ['5s',
    '10s',
    '30s',
    '1m',
    '5m',
    '15m',
    '30m',
    '1h',
    '2h',
    '1d'],
   'time_options': ['5m', '15m', '1h', '6h', '12h', '24h', '2d', '7d', '30d']},
  'timezone': '',
  'title': 'Python Dashboard',
  'uid': '-0BCN4sWz',
  'version': 15},
 'meta': {'canAdmin': False,
  'canEdit': True,
  'canSave': True,
  'canStar': True,
  'created': '2020-01-21T07:39:23Z',
  'createdBy': 'admin',
  'expires': '0001-01-01T00:00:00Z',
  'folderId': 0,
  'folderTitle': 'General',
  'folderUrl': '',
  'hasAcl': False,
  'isFolder': False,
  'provisioned': False,
  'provisionedExternalId': '',
  'slug': 'python-dashboard',
  'type': 'db',
  'updated': '2020-01-21T17:26:03Z',
  'updatedBy': 'admin',
  'url': '/d/-0BCN4sWz/python-dashboard',
  'version': 15}}

print("Update Table")
grafana_table_dashboard_json['dashboard']['panels'][0]['targets'][0]['rawSql'] = rawQwery
print("Update Map")
grafana_table_dashboard_json['dashboard']['panels'][1]['targets'][0]['rawSql'] = rawQwery

# Create or update a dashboard
# grafana_api.dashboard.update_dashboard(dashboard={'dashboard': {...}, 'folderId': 0, 'overwrite': True})
update = True
if update == True:
  if 'overwrite' not in grafana_table_dashboard_json.keys(): # make sure to overwrite not to have any issue
    grafana_table_dashboard_json['overwrite'] = True
  grafana_api.dashboard.update_dashboard(grafana_table_dashboard_json)
  print("Dashboard is updated!!")

