import markdown
import os
import shelve
import sys

# Observatory Service

# Import framework
from flask import Flask, jsonify, make_response, Response, json, request
from flask_restful import Resource, Api

from datetime import datetime
import pandas as pd

from dateutil.relativedelta import relativedelta
from datetime import date, time

import json



# Instantiate the app
app = Flask(__name__)
api = Api(app)

# Creation Of Main Endpoint Classes
class Test(Resource):
    def post(self):
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


        # Get POST data as json & read it as a DataFrame
        new_x = request.get_json()

        current_data = pd.read_json(json_str)
        return json_str# {'message': 'POST data read successfully'}

# Addition of the Endpoint Classes As Endpoints For The RESTFul API
api.add_resource(Test, '/api/v1')


class Observatory(Resource):
    def get(self):
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
        json_str
        def set_default(obj):
            if isinstance(obj, set):
                return list(obj)
            raise TypeError

        result = json.dumps(json_str, default=set_default)
        result = jsonify(json_str)
        resp = make_response(df.to_json(orient = "records"))
        demo = {
                'key': df.to_dict(orient='record')
            }

        return jsonify([{"Name":"AOV039","Code":"AOV039","Start":"2019-09-17 17:30","DOY":260.0,"Dur":"24:00","Stations":"Ho  Is  K1  Kg  Sh  Sy  Vm  Ww  Yg  Ke","DB Code":"XA","Ops Center":"GSI","Correlator":"GSI","Status":null,"Analysis":"NASA","start_date":1568678400000,"start_time":"17:30:00","Split_Stations":["Ho","Is","K1","Kg","Sh","Sy","Vm","Ww","Yg","Ke"]}])
        #json.dumps(demo)

# Create routes
api.add_resource(Observatory, '/')

# Run the application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)