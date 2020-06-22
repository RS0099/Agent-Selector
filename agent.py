#!/usr/bin/env python3

import csv
import operator
import collections
import random
from datetime import datetime

agents_list=[]
agent_no_in_list={}

#used maximum functions

def generate_agents_list():
	with open('agents.csv','r') as file:
		fields=file.readline().strip().split(',')
		agents=csv.DictReader(file,',')
		agents.fieldnames=fields
		counter=0
		for agent in agents:
			temp_agent={}
			for field in fields:
				temp_agent[field]=agent[field].split('|')
			agents_list.append(temp_agent)
			agent_no_in_list[agent['name']]=counter
			counter=counter+1
		
	return


def generate_issue_agent_list(issue_roles):
	issue_agent_time_list={}
	no_of_role=len(issue_roles)
	counter=0
	for agent in agents_list:
		if agent['is_available'][0]=='1':
			counter=0
			for role in issue_roles:
				if role in agent['roles']:
					counter=counter+1
			if counter==no_of_role:
				issue_agent_time_list[agent['name'][0]]=agent['available since'][0]
	issue_agent_time_list=sorted(issue_agent_time_list.items(),key=operator.itemgetter(1))
	#issue_agent_time_list=collections.OrderedDict(issue_agent_time_list)

	issue_agent_list=[]

	for agent in issue_agent_time_list:
		issue_agent_list.append(agent[0])

	return issue_agent_list

def list_on_selection(selection_mode,issue_roles):
	agent_list=generate_issue_agent_list(issue_roles)

	final_list=[]
	if len(agent_list)==0:
		final_list.append("Sorry no agent available")
	elif selection_mode=="least busy":
		final_list.append(agent_list[0])
	elif selection_mode=="random":
		no_of_agent=len(agent_list)
		agent_no=random.randint(0,no_of_agent-1)
		final_list.append(agent_list[agent_no])
	elif selection_mode=="all available":
		final_list.extend(agent_list)
	else :
		final_list.append("Please enter a valid selection mode")

	return final_list

def update_agent_list(agent,update_type):
	if update_type=="available":
		agents_list[agent_no_in_list[agent]]['is_available']=1
		now=datetime.now()
		agents_list[agent_no_in_list[agent]]['available_since']=str(now)
	# time format 	'2020-06-22 16:33:23.296332'
	elif update_type=="busy":
		agents_list[agent_no_in_list[agent]]['is_available']=0
	else :
		print("Wrong update type")
	return	


def solve_issues():
	file= open('agent_alloted_list.csv','w',newline='')
	writer=csv.writer(file)
	with open('issues.csv','r') as issues:
		fields=issues.readline().strip().split(',')
		issues_list=csv.DictReader(issues,',')
		issues_list.fieldnames=fields
		for issue in issues_list:
			agent_list=list_on_selection(issue['selection type'],issue['roles'].split('|'))
			writer.writerow(agent_list)
	file.close()	
	return

generate_agents_list()
solve_issues()
# you can update if you want :)

