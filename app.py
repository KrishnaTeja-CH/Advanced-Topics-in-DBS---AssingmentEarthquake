import textwrap

from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import pandas as pd
import pyodbc
import numpy as np

app = Flask(__name__)

driver = '{ODBC Driver 17 for SQL Server}'
server_name = 'thedomain'
database_name = 'Krishna'
username = "itsmekt"
password = "******"
server = '{server_name}.database.windows.net,1433'.format(server_name=server_name)
connection_string = textwrap.dedent('''
    Driver={driver};
    Server={server};
    Database={database};
    Uid={username};
    Pwd={password};
    Encrypt=yes;
    TrustServerCertificate=no;
    Connection Timeout=30;
'''.format(
    driver=driver,
    server=server,
    database=database_name,
    username=username,
    password=password
))
conn = pyodbc.connect(connection_string)
cursor = conn.cursor()


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/eqnet', methods=['GET', 'POST'])
def eq_net():
    earthquakes = []
    earthquakes1 = []
    if request.method == 'POST':
        start_time = request.form.get('stime')
        stop_time = request.form.get('sttime')
        net_value = request.form.get('netv')

    cursor.execute("select time, time2, latitude, longitude, place, net, mag from q where time2>? and time2 < ? and net = ?",start_time, stop_time, net_value)
    for data in cursor:
        earthquakes.append(data)
    earthquake_len = len(earthquakes)

    cursor.execute("select Top 3 time, time2, latitude, longitude, place, net, mag from q where time2 between ? and ? AND net= ? order by Mag desc",start_time, stop_time, net_value)
    for data in cursor:
        earthquakes1.append(data)
    earthquake_len1 = len(earthquakes1)
    return render_template("eq_net.html", earthquakes=earthquakes, length=earthquake_len, earthquakes1=earthquakes1, length1=earthquake_len1)


if __name__ == '__main__':
    app.run()
