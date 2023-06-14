import os
import datetime
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import subprocess
import yaml
print('Import deeplabcut')
import deeplabcut as dlc  

"""Creates a unique folder name if there is already a folder with the same name"""
def creat_unique_folder():
	global current_directory, name, project_name, date, folder_name
	current_directory = os.path.dirname(os.path.abspath(__file__))
	#print(current_directory)
	"""Sets standard names of the project"""
	name = 'unknown'
	project_name = 'new_project'
	date = datetime.date.today()
	folder_name = project_name + '-' + name + '-' + str(date)
	print('Folder name:', folder_name)
	suffix = 1
	suffax = 0
	while True:
		"""If there is a folder with the same name"""
		if os.path.exists(os.path.join(current_directory, folder_name)):
			"""If the folder has its own unique number, then increase it by one"""
			if f'({suffax})' in folder_name:
				project_name = project_name.replace(f'({suffax})', f'({suffix})')
			"""If the folder does not have its own unique number, add one"""
			else:
				project_name = f"{project_name}({suffix})"
			"""Changes the old name to the new name and adds +1 to the value"""
			folder_name = project_name + '-' + name + '-' + str(date)
			suffix += 1
			suffax += 1
		"""If the name is unique, it creates a path to the config"""
		elif not os.path.exists(os.path.join(current_directory, folder_name)):
			global config_path
			config_path = current_directory+'/'+folder_name+'/config.yaml'
			break

#print('New name: ' + folder_name)
#print('Project name: '+ project_name)
#print('The video folder is empty:', videos_list)

"""Processes video data"""
def list_videos():
	global videos_list
	videos_list = []
	"""Creates a list where the name of the video and the path to them will be stored"""
	if not os.path.exists(os.path.join(current_directory, 'video')):
		"""Creates a "video" folder if there is none"""
		os.makedirs(os.path.join(current_directory, 'video'))
		print('Folder "video" has been created at ' + current_directory)
		while True:
			"""Give the time to place the video in the foler"""
			x = str(input('Place the video at the folder and type "y" to continue '))
			if x.lower() == 'y':
				break
	files = os.listdir(os.path.join(current_directory, 'video'))
	while True:
		"""Working with the video folder"""
		for filename in files:
			"""Check if the video has a good video type. If yes, it is added to 'videos_list' with the path"""
			if filename.endswith('.mp4') or filename.endswith('.avi'):
				videos_list.append(os.path.join(current_directory, 'video', filename))
		if len(videos_list) == 0:
			"""If the "video" folder is empty"""
			print('Folder "video" is empty. Please put your videos there')
			while True:
				"""Give the time to place the video in the foler"""
				x = str(input('Place the video at the folder and write "y" to continue '))
				if x.lower() == 'y':
					break
		else:
			"""If the "video" folder have the video name and path"""
			break

#print('The videos in the video folder:', videos_list)

"""Works with the names of the bodyparts"""
def ask_for_bodyparts():
	"""Open the config file"""
	with open(config_path, "r") as file:
		data = yaml.safe_load(file)
	"""Replace the standart names to my standart names"""
	new_bodyparts = ['nose', 'leftear', 'rightear', 'tailbase']
	data["bodyparts"] = new_bodyparts
	x = str(input('Write the bodyparts with backspace like "nose leftear". If don\'t want to change, write nothing\n'))
	"""If don't want to change"""
	if len(x) == 0:
		print('You write nothing')
	"""If the user have writed his own bodyparts names"""
	else:
		new_bodyparts = x.split()
		data["bodyparts"] = new_bodyparts
	"""Save the data in the config file"""
	with open(config_path, "w") as file:
		yaml.safe_dump(data, file)

root = Tk()
root.withdraw()
"""Makes it so that the interface will work"""

"""Begin of the code"""
while True:
	x = str(input(('Start creating new project and lebel it?(y/n) ')))
	"""If the user want to make a project and label it"""
	if x.lower() == 'y':
		creat_unique_folder()
		list_videos()
		print('Creat new project')
		dlc.create_new_project(project_name, name, videos_list, working_directory=current_directory, copy_videos=True, multianimal=False)
		ask_for_bodyparts()
		"""Ask if he want to continue after the changing of the config file"""
		while True:
			x = str(input('"y" to continue (config file modifing)'))
			if x.lower() == 'y':
				break
		print('Chose the config file in:', current_directory+'\\'+folder_name)
		print("old config path", config_path)
		#config_path = askopenfilename()
		print("new config path", config_path)
		print('Ectract frames')
		dlc.extract_frames(config_path, mode='automatic', algo='kmeans', userfeedback=False, crop=False)
		print('Begin labeling.\nPlace the points')
		dlc.label_frames(config_path)
		"""Stops to place the points in napari"""
		while True:
			x = str(input('"y" to continue (label)'))
			if x.lower() == 'y':
				break
		print('Cheking labels')
		dlc.check_labels(config_path, visualizeindividuals=False)
		break
	"""If the user already have a project with labeled data"""
	elif x.lower() == 'n':
		x = str(input(('Start creating a dataset and train the network?(y/n) ')))
		"""If the user want to creat a dataset and train the network"""
		if x.lower() == 'y':
			config_path = askopenfilename()
			print('Making a dataset for training')
			input()
			dlc.create_training_dataset(config_path, augmenter_type='imgaug')
			print('Begin training')
			dlc.train_network(config_path)
			break
		"""If the user want to leave the code"""
		elif x.lower() == 'n':
			print('I finish the code. Bye')
			break