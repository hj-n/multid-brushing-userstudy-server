from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

import os, json


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite'
db = SQLAlchemy(app)
CORS(app)

"""
CONSTANTS
"""

EXP1_TRIAL_INFOS = None

"""
Models for the database
"""




"""
Functions for the API
"""


## for test
@app.route('/', methods=['GET'])
def hello_world():
	return 'Hello, World!'

## for delivering the task information
@app.route('/gettrialinfo', methods=['GET'])
def get_trial_info():
	args = request.args
	participant_num = args.get('participant_num')
	trial_num = int(args.get('trial_num'))
	exp_num = int(args.get('exp_num'))

	if exp_num == 1:
		results = EXP1_TASK_INFOS["P" + participant_num][trial_num]
	else:
		pass

	return jsonify(results)

@app.route('/getpreprocesseddata', methods=['GET'])
def get_preprocessed_data():
	args = request.args
	identifier = args.get('identifier')
	exp_num = int(args.get('exp_num'))

	if exp_num == 1:
		with open(f"./data/exp1/preprocessed/{identifier}.json", 'r') as f:
			results = json.load(f)
	return jsonify(results)

if __name__ == '__main__':

	EXP1_TASK_INFOS = json.load(open('./data/exp1/trial_infos_exp1.json', 'r'))

	app.run(debug=True)

