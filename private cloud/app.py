# import the Flask class from the flask module
from flask import Flask, render_template,redirect, url_for, request,jsonify
import sqlite3
from sqlite3 import Error
import json
import requests
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)

app = Flask(__name__)

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn


@app.route('/welcome')
def welcome():
    return render_template('welcome.html')  # render a template


@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    cloud={'cloud_red' : ['http://192.168.43.101:5000', 'abcd'], 'cloud_blue' :['http://192.168.43.101:5001','efgh']}

    database= r"company.db"
    if request.method == 'POST':
        conn = create_connection(database)

        with conn:
            cur=conn.cursor()
            emailId=request.form['emailId']
            cur.execute("select * from employee where emailId=?",(emailId,))
            row=cur.fetchall()[0]
            password=row[1]

            if request.form['password'] != password:
                error = 'Invalid Credentials. Please try again.'
            else:
                cloud_service=request.form['option']
                if cloud_service=="cloud_red":
                    role=row[2]
                else:
                    role=row[3]

                res= requests.post(cloud[cloud_service][0]+'/home', data={"username":emailId, "role":role,"key":cloud[cloud_service][1]}, headers={"Content-Type":"application/json"})
                url = res.json()["url"]
                if res.json()["status"]=='1000':
                    return "Fatal error. Key verification failed."
                elif res.json()["status"]=='1002':
                    return "Fatal error. You do not have an account in this cloud."

                #return cloud[cloud_service]+url
                return redirect(cloud[cloud_service][0]+url)
    return render_template('login.html', error=error)


if __name__ == '__main__':
    app.run(host='localhost',port=5000,debug=True)
