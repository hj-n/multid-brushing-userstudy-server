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
EXP2_TRIAL_INFOS = None

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
	elif exp_num == 2:
		results = EXP2_TASK_INFOS["P" + participant_num][trial_num]
	

	return jsonify(results)

@app.route('/getpreprocesseddata', methods=['GET'])
def get_preprocessed_data():
	args = request.args
	identifier = args.get('identifier')
	exp_num = int(args.get('exp_num'))

	if exp_num == 1:
		with open(f"./data/exp1/preprocessed/{identifier}.json", 'r') as f:
			results = json.load(f)
	elif exp_num == 2:
		with open(f"./data/exp2/preprocessed/{identifier}.json", 'r') as f:
			results = json.load(f)
	return jsonify(results)

@app.route('/postbrushingresult', methods=["POST"])
def post_brushing_result():
	args = request.args
	brushedIndex = args.get('brushedIndex')
	completionTime = args.get('completionTime')
	
	identifier = args.get('identifier')
	participant_num = args.get('participant')
	trial_num = args.get('trial')
	exp_num = int(args.get('exp'))

	print(exp_num, participant_num, trial_num, identifier)

	## change brushedIndex to list
	brushedIndexList = brushedIndex.split(",")
	if brushedIndexList[0] == "":
		brushedIndexList = []
	brushedIndexList = [int(i) for i in brushedIndexList]
	completionTime = float(completionTime)

	result = {
		"brushedIndex": brushedIndexList,
		"completionTime": completionTime,
		"identifier": identifier,
	}

	## save the result
	if exp_num == 1:
		with open(f"./data/exp1/results/{participant_num}_{trial_num}.json", 'w') as f:
			json.dump(result, f)
	
	elif exp_num == 2:
		with open(f"./data/exp2/results/{participant_num}_{trial_num}.json", 'w') as f:
			json.dump(result, f)


	return "Success"



@app.route('/postsurveyresult', methods=["POST"])
def post_survey_result():
	args = request.args
	age = args.get('age')
	gender = args.get('gender')
	education = args.get('education')
	major = args.get('major')
	famil_vis = args.get('familVis')
	famil_scatter = args.get('familScatter')
	participant_num = args.get('participant')

	result = {
		"age": age,
		"gender": gender, 
		"education": education,
		"major": major,
		"familVis": famil_vis,
		"familScatter": famil_scatter,
	}

	with open(f"./data/exp1/survey/{participant_num}.json", 'w') as f:
		json.dump(result, f)
	
	return "Success"



if __name__ == '__main__':

	EXP1_TASK_INFOS = json.load(open('./data/exp1/trial_infos_exp1.json', 'r'))
	EXP2_TASK_INFOS = json.load(open('./data/exp2/trial_infos_exp2.json', 'r'))

	app.run(debug=True, port=5100)


