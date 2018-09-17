#!/usr/local/bin/python
# -*- coding: iso-8859-15 -*-

#Imports the Flask library, making the code available to the rest of the application.#
import os
import flask
from flask import request, jsonify
from flask import Flask
from flask_cors import CORS
import requests
import sqlite3

#Creates the Flask application object, which contains data about the application and also methods (object functions) that tell the application to do certain actions
app = flask.Flask(__name__)
CORS(app)

#Starts the debugger. With this line, if your code is malformed, you’ll see an error when you visit your app
app.config["DEBUG"] = True



def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

@app.route('/', methods=['GET'])
def home():
    return '''<h1>Data API for k9-1-1 iot devices</h1>
<p>A prototype API for retrieving k9-1-1 iot device data.</p>'''

@app.route('/alerts', methods=['POST'])
def alerts():
    # pull the serial number from request.data
    num = request.data.serialNum
    userIdResponse = requests.get('http://localhost:3911/devices_users?serialNum={num}')
    jsonUserIdResponse = response.json()


    return '''<h1>hit /alerts POST route</h1>'''

#Define Admin route to get all devices.
@app.route('/k911/v1/devices/all', methods=['GET'])
def api_all():
    #connect to the database using our sqlite3 library and an object representing the connection to the database is bound to the conn variable
    conn = sqlite3.connect('devices.db')

    #tells the connection object to use the dict_factory function that we've defined which returns items from the database as dictionaries rather than lists as these work better when we output them to JSON
    conn.row_factory = dict_factory

    #on this line we create a cursor object which is the object that actually moves through the database to pull our data
    cur = conn.cursor()

    #execute an SQL query with the cur.execute method to pull out all available data (*) from the books table of our database
    all_devices = cur.execute('SELECT * FROM devices;').fetchall()

    #return this data as JSON
    return jsonify(all_devices)

#Create error handler which will display a page seen by the user if the user encounters an error or inputs a route that hasn’t been defined
@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404

@app.route('/k911/v1/devices/:device_id', methods=['GET'])
def api_filter():
    #The function first grabs all the query parameters provided in the URL (remember, query parameters are the part of the URL that follows the ?, like ?id=10)
    query_parameters = request.args

    #It then pulls the supported parameter device_id and binds it to an appropriate variable
    device_id = query_parameters.get('device_id')

    #Next we will build an SQL query that will be used to find the requested information in the database. SQL queries used to find data in a database take this form `SELECT <columns> FROM <table> WHERE <column=match> AND <column=match>;`
    # define both the query and the filter list
    query = "SELECT * FROM devices WHERE"
    to_filter = []

    #if device_id, was provided as a query parameter, we add it to both the query and the filter list:
    if device_id:
        query += ' device_id=? AND'
        to_filter.append(device_id)

    #If the user didn't provide a device_id as a query parameter, we have nothing to show, so we send them to the “404 Not Found” page
    if not (device_id):
        return page_not_found(404)

    #To perfect our query, we remove the trailing ` AND and cap the query with the ;` required at the end of all SQL statements
    query = query[:-4] + ';'

    #we connect to our database as in our api_all function, then execute the query we’ve built using our filter list
    conn = sqlite3.connect('devices.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()

    results = cur.execute(query, to_filter).fetchall()

    # Use the jsonify function from Flask to return the results of our executed SQL query as JSON to the user
    return jsonify(results)

app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
