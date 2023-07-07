import os
import datetime
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import subprocess
import yaml
import shutil
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
print('Import deeplabcut')
import deeplabcut as dlc 

#sets the current_directory and the time
current_directory = os.path.dirname(os.path.abspath(__file__))
date = datetime.date.today()

#sets the valid parameters
dataset_valid = ["num_shuffles","Shuffles","userfeedback","trainIndices","testIndices","net_type","augmenter_type","posecfg_template"]
network_valid = ["shuffle","trainingsetindex","max_snapshots_to_keep","displayiters","saveiters","maxiters","allow_growth","gputouse","autotune","keepdeconvweights","modelprefix"]
together_valid = dataset_valid+network_valid

print('Open config.json')
with open(os.path.join(current_directory, 'config.json'), 'r') as file:
	option = json.load(file)
print('Finished open config file\nCalculate the numbers')
def option_taking(valid):
	numbers = {}
	r = 1
	dubl_numbers={}
	for key, value in option.items():
		if key in valid:
			numbers[key]=len(value)
	for value in numbers.values():
		r *= value
	for key, value in option.items():
		if key in valid:
			dubl_numbers[key] = np.tile(value, r//numbers[key])
	return dubl_numbers, r

dataset_n, dataset_r = option_taking(dataset_valid)
network_n, network_r = option_taking(network_valid)
together_n, together_r = option_taking(together_valid)
print('Finished calculate numbers')

print(dataset_n)
print(network_n)
print(together_n)
print('\n')
print(dataset_r)
print(network_r)
print(together_r)

def unique_name(name, directory):
	suffix = 1
	while True:
		#If there is a folder with the same name
		if os.path.exists(os.path.join(directory, name)):
			#If the folder has its own unique number, then increase it by one
			if f'({suffix})' in name:
				name = name.replace(f'({suffix})', f'({suffix+1})')
				suffix+=1
			#If the folder does not have its own unique number, add one
			else:
				name = f"{name}({suffix})"
		#If the name is unique, it creates a path to the config
		elif not os.path.exists(os.path.join(directory, name)):
			return name

print("Making folder and save path")
working_place_name = option["project_name"] + '-' + option["name"] + '-' + str(date)
directory_working_place = os.path.join(current_directory, unique_name(working_place_name, current_directory))
os.makedirs(directory_working_place)
print('Finished making folder')

#list with the required folders and files
required_folders = ["videos", "labeled-data"]
required_files = ["config.yaml"]

#Checks the presence of the necessary folders and files, as well as the contents of folders
print('Cheking the required folders')
while True:
	labeled_project_path = option["labeled_project_path"]
	# Checking for folders
	missing_folders = [folder for folder in required_folders if not os.path.exists(os.path.join(labeled_project_path, folder))]
	if missing_folders:
		print("The following folders are missing:")
		for folder in missing_folders:
			print(folder)
	else:
		# Checking for file availability
		missing_files = [file for file in required_files if not os.path.exists(os.path.join(labeled_project_path, file))]
		if missing_files:
			print(f"Missing file: {required_files}")
			for file in missing_files:
				print(file)
		else:
			# Checking empty folders
			empty_folders = [folder for folder in required_folders if os.path.exists(os.path.join(labeled_project_path, folder)) and not os.listdir(os.path.join(labeled_project_path, folder))]
			if empty_folders:
				print("The following folders are empty:")
				for folder in empty_folders:
					print(folder)
			else:
				break
	input("Press Enter to continue...")
print('Finished cheking')

#Adds video paths to the list
def list_videos(directory, chose):
	videos_list = []
	if chose == True:
		files = os.listdir(os.path.join(labeled_project_path, 'videos'))
		os.makedirs(os.path.join(directory,'videos'))
		while True:
			print('Cheking videos')
			for filename in files:
				#Check if the video has a good video type. If yes, it is added to 'videos_list' with the path
				if filename.endswith('.mp4') or filename.endswith('.avi'):
					print("Succes")
					shutil.copy(os.path.join(labeled_project_path,'videos',filename), os.path.join(directory,'videos',filename))
					videos_list.append(os.path.join(directory, 'videos', filename))
			if len(videos_list) == 0:
				#If the "video" folder is empty
				print('Folder "videos" have invalide video type. Please put valide videos (mp4 or avi)')
				while True:
					#Give the time to place the video in the foler
					input('Place the videos at the folder and press "Enter" to continue')
					break
			else:
				return videos_list
	else:
		files = os.listdir(os.path.join(directory, 'videos'))
		for filename in files:
			if filename.endswith('.mp4') or filename.endswith('.avi'):
				videos_list.append(os.path.join(directory, 'videos', filename))
		return videos_list

print('Save videos path')
videos_list	= list_videos(directory_working_place, True)
print('Finished saving videos path\nBegin the project')

"""
print(videos_list)
print('Number of dataset:', dataset_r)
print('Number of network:', network_r)
print('Number of all:', together_r)
"""

lebaled_folder = os.path.join(labeled_project_path,'labeled-data')
def change_config_file(config_path):
	#Open the config file
	with open(config_path, "r") as file:
		old_data = yaml.safe_load(file)
	with open(os.path.join(labeled_project_path,'config.yaml'), "r") as file:
		new_data = yaml.safe_load(file)
	#Replace the standart names to my standart names
	old_data["bodyparts"] = new_data['bodyparts']
	old_data['scorer'] = new_data['scorer']
	#Save the data in the config file
	with open(config_path, "w") as file:
		yaml.safe_dump(old_data, file)

def none_check(con, sum):
	con()

num=0
while not num == dataset_r:
	print('Dataset number:', num+1)
	project_name=option["project_name"]
	"""
	for key, value in dataset_n.items():
		project_name = f'{project_name}_{key}={value[num]}'
	"""
	unique_name(project_name, directory_working_place)
	folder_name = project_name+'-'+option["name"]+'-'+str(date)
	print('Create project', folder_name)
	dlc.create_new_project(project_name, option["name"], videos_list, working_directory=directory_working_place, copy_videos=True, multianimal=False)
	directory_folder_place = os.path.join(directory_working_place, folder_name)
	print(f'Project {project_name} created\nChange folder and config set')
	lebaled_folder_false = os.path.join(directory_folder_place, 'labeled-data')
	config_path = os.path.join(directory_folder_place, 'config.yaml')
	shutil.rmtree(lebaled_folder_false)
	shutil.copytree(lebaled_folder, lebaled_folder_false)
	change_config_file(config_path)
	print('Changing done\nMaking a dataset for training')
	dlc.create_training_dataset(config_path,
		num_shuffles=int(dataset_n["num_shuffles"][num]) if dataset_n["num_shuffles"][num] is not None else 1,
		Shuffles=list(dataset_n["Shuffles"][num]) if dataset_n["Shuffles"][num] is not None else None,
		userfeedback=bool(dataset_n["userfeedback"][num]) if dataset_n["userfeedback"][num] is not None else False,
		trainIndices=str(dataset_n["trainIndices"][num]) if dataset_n["trainIndices"][num] is not None else None,
		testIndices=str(dataset_n["testIndices"][num]) if dataset_n["testIndices"][num] is not None else None,
		augmenter_type=str(dataset_n["augmenter_type"][num]) if dataset_n["augmenter_type"][num] is not None else None,
		net_type=str(dataset_n["net_type"][num]) if dataset_n["net_type"][num] is not None else None,
		posecfg_template=str(dataset_n["posecfg_template"][num]) if dataset_n["posecfg_template"][num] is not None else None)
	print('Finished creating dataset.\nBegin training')
	num+=1
	num2=0
	while not num2 == network_r:
		print('Network number:', num2+1)
		dlc.train_network(config_path,
			shuffle = int(network_n["shuffle"][num2]) if network_n["shuffle"][num2] is not None else 1,
			trainingsetindex = int(network_n["trainingsetindex"][num2]) if network_n["trainingsetindex"][num2] is not None else 0,
			max_snapshots_to_keep = int(network_n["max_snapshots_to_keep"][num2]) if network_n["max_snapshots_to_keep"][num2] is not None else None,
			displayiters = int(network_n["displayiters"][num2]) if network_n["displayiters"][num2] is not None else None,
			saveiters = int(network_n["saveiters"][num2]) if network_n["saveiters"][num2] is not None else None,
			maxiters = int(network_n["maxiters"][num2]) if network_n["maxiters"][num2] is not None else None,
			allow_growth = bool(network_n["allow_growth"][num2]) if network_n["allow_growth"][num2] is not None else True,
			gputouse = str(network_n["gputouse"][num2]) if network_n["gputouse"][num2] is not None else None,
			autotune = bool(network_n["autotune"][num2]) if network_n["autotune"][num2] is not None else False,
			keepdeconvweights = bool(network_n["keepdeconvweights"][num2]) if network_n["keepdeconvweights"][num2] is not None else True)
			#modelprefix = str(network_n["modelprefix"][num2]) if network_n["modelprefix"][num2] is not None else None
		print('Finished train the network.\nBegin evaluate network')
		dlc.evaluate_network(config_path, Shuffles=[1], plotting=True)
		print('Finished evaluate network.\nBegin analyze videos')
		videos_list2 = list_videos(directory_folder_place, False)
		dlc.analyze_videos(config_path, videos_list2, save_as_csv=True)
		print('Finished analyze videos\n')
		dlc.filterpredictions(config_path, videos_list2)
		dlc.plot_trajectories(config_path, videos_list2)
		num2+=1
	print()
	continue
	project_number = 1
	results = {}
	results[project_number] = {

	}

"""
def analays_results():
"""

