import json
import os
import sqlite3

# Third-party libraries
from flask import Flask, redirect, render_template,request, jsonify,url_for
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)

import requests
from random import randint
# Internal imports


app = Flask(__name__)


roles_dict={
	"compute": [1,0,0],
	"storage": [0,1,0],
	"database": [0,0,1],
	"full_access": [1,1,1],
	"storage_compute":[1,1,0]
}




id = 'default'
roles = 'default'
token = ''
key = 'default'
def generate_token():
	global token
	tok = ''
	for i in range(32):
		r = randint(0,2)
		if r== 0:
			tok+= chr(randint(65, 90))
		elif r == 1:
			tok+= chr(randint(48, 57))
		else:
			tok+= chr(randint(97,122))
	token = tok
	return tok

@app.route("/manage")
def manage():
	code = request.args['data']
	if code != token:
		return render_template('failed.html')
	permissions = [['Red Compute Plus',1], ['Red Storage 5',1], ['Red Database SQL',1]]
	
	for i in range(len(roles_dict[roles])):
		permissions[i][1] = permissions[i][1]*roles_dict[roles][i]
	return render_template('home.html', identity=id, permissions=permissions)

key_base = ["abcd"]
	
	
@app.route("/home", methods=['POST'])
def home():
	global id
	global roles
	global key
	to_send = generate_token()
	
	user = request.json
	print(user)
	if len(user)<3:
		message = {"url": "", "status": "1002"}
		response = app.response_class(response=json.dumps(message),status=200,mimetype='application/json')
		return response
	
	#id = user[0].split('=')[1]
	#roles = user[1].split('=')[1]
	#key = user[2].split('=')[1][:-1]
	id = user["name"]
	roles=  user["role"]
	key = user["key"]
	if key!= key_base[0]:
		message = {"url": "", "status": "1000"}
		response = app.response_class(response=json.dumps(message),status=200,mimetype='application/json')
		return response
	url = {"url":url_for('manage', data=to_send), "status":"1001"}		#data is the value that will be taken from the url
	
	#return jsonify({'you_sent': data}), 201
	response = app.response_class(
        response=json.dumps(url),
        status=200,
        mimetype='application/json'
    )
	return response
	
	
	
@app.route("/logout")
def logout():
	return 'You have been successfully logged out'



if __name__ == "__main__":
    app.run(host='127.0.0.1', port= 5000,debug=True)
