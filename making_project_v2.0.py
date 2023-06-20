import os
import datetime
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import subprocess
import yaml
import shutil
print('Import deeplabcut')
import deeplabcut as dlc 

#TEMPORALY DOESN'T WORK!!!!!!!!!


chose_names = False
chose_names_dubl = False
chose_names_copys = False
chose_bodyparts = True

current_directory = os.path.dirname(os.path.abspath(__file__))

#Creates a unique folder name if there is already a folder with the same name
def creat_unique_folder():
	global name, project_name, date, folder_name
	#print(current_directory)
	#Sets standard names of the project
	name = 'unknown'
	if chose_names == False:
		project_name = 'new_project'
	else:
		if chose_names_dubl == False:
			project_name = 'origin_folder4'
		else:
			if chose_names_copys == False:
				project_name = 'copy_folder4'
			else:
				project_name = 'copy_folder4.2'
	date = datetime.date.today()
	folder_name = project_name + '-' + name + '-' + str(date)
	print('Folder name:', folder_name)
	suffix = 1
	suffax = 0
	while True:
		#If there is a folder with the same name
		if os.path.exists(os.path.join(current_directory, folder_name)):
			#If the folder has its own unique number, then increase it by one
			if f'({suffax})' in folder_name:
				project_name = project_name.replace(f'({suffax})', f'({suffix})')
			#If the folder does not have its own unique number, add one
			else:
				project_name = f"{project_name}({suffix})"
			#Changes the old name to the new name and adds +1 to the value
			folder_name = project_name + '-' + name + '-' + str(date)
			suffix += 1
			suffax += 1
		#If the name is unique, it creates a path to the config
		elif not os.path.exists(os.path.join(current_directory, folder_name)):
			global config_path
			config_path = current_directory+'/'+folder_name+'/config.yaml'
			break

#print('New name: ' + folder_name)
#print('Project name: '+ project_name)
#print('The video folder is empty:', videos_list)

#Processes video data
def list_videos():
	global videos_list
	current_directory_for_list_videos = os.path.dirname(os.path.abspath(__file__))
	videos_list = []
	#Creates a list where the name of the video and the path to them will be stored
	if not os.path.exists(os.path.join(current_directory_for_list_videos, 'video')):
		#Creates a "video" folder if there is none
		os.makedirs(os.path.join(current_directory_for_list_videos, 'video'))
		print('Folder "video" has been created at ' + current_directory_for_list_videos)
		while True:
			#Give the time to place the video in the foler
			x = str(input('Place the video at the folder and type "y" to continue '))
			if x.lower() == 'y':
				break
	files = os.listdir(os.path.join(current_directory_for_list_videos, 'video'))
	while True:
		#Working with the video folder
		for filename in files:
			#Check if the video has a good video type. If yes, it is added to 'videos_list' with the path
			if filename.endswith('.mp4') or filename.endswith('.avi'):
				videos_list.append(os.path.join(current_directory_for_list_videos, 'video', filename))
		if len(videos_list) == 0:
			#If the "video" folder is empty
			print('Folder "video" is empty. Please put your videos there')
			while True:
				#Give the time to place the video in the foler
				x = str(input('Place the video at the folder and write "y" to continue '))
				if x.lower() == 'y':
					break
		else:
			#If the "video" folder have the video name and path
			break

#print('The videos in the video folder:', videos_list)

#Works with the names of the bodyparts
def ask_for_bodyparts():
	#Open the config file
	with open(config_path, "r") as file:
		data = yaml.safe_load(file)
	#Replace the standart names to my standart names
	new_bodyparts = ['nose', 'leftear', 'rightear', 'tailbase']
	data["bodyparts"] = new_bodyparts
	if chose_bodyparts == True:
		x = str(input('Write the bodyparts with backspace like "nose leftear". If don\'t want to change, write nothing\n'))
		#If don't want to change
		if len(x) == 0:
			print('You write nothing')
		#If the user have writed his own bodyparts names
		else:
			new_bodyparts = x.split()
			data["bodyparts"] = new_bodyparts
	#Save the data in the config file
	with open(config_path, "w") as file:
		yaml.safe_dump(data, file)

def unique_folder_projects_name(project_folder_name):
	suffix = 1
	suffax = 0
	while True:
		#If there is a folder with the same name
		if os.path.exists(os.path.join(current_directory, project_folder_name)):
			#If the folder has its own unique number, then increase it by one
			if f'({suffax})' in project_folder_name:
				project_folder_name = project_folder_name.replace(f'({suffax})', f'({suffix})')
			#If the folder does not have its own unique number, add one
			else:
				project_folder_name = f"{project_folder_name}({suffix})"
			#Add +1 to the value
			suffix += 1
			suffax += 1
		#If the name is unique, it creates a path to the config
		elif not os.path.exists(os.path.join(current_directory, project_folder_name)):
			break
	os.makedirs(os.path.join(current_directory, project_folder_name))
	return project_folder_name

root = Tk()
root.withdraw()
#Makes it so that the interface will work

#Begin of the code
while True:
	print('1 = Start creating new project and label it')
	print('2 = Start creating a dataset and train the network')
	print('3 = Start creating a labeled video')
	print('4 = Start creating 10 project and do the 1 and 2 part')
	print('q = quit the code')
	x = str(input(('Type the number what you want to do: ')))
	#If the user want to make a project and label it
	if x.lower() == '1':
		creat_unique_folder()
		list_videos()
		print('Creat new project')
		dlc.create_new_project(project_name, name, videos_list, working_directory=current_directory, copy_videos=True, multianimal=False)
		ask_for_bodyparts()
		#Ask if he want to continue after the changing of the config file
		while True:
			x = str(input('"y" to continue (config file modifing)'))
			if x.lower() == 'y':
				break
		print('Chose the config file in:', current_directory+'/'+folder_name)
		print("old config path", config_path)
		#config_path = askopenfilename()
		print("new config path", config_path)
		print('Ectract frames')
		dlc.extract_frames(config_path, mode='automatic', algo='kmeans', userfeedback=False, crop=False)
		print('Begin labeling.\nPlace the points')
		dlc.label_frames(config_path)
		#Stops to place the points in napari
		while True:
			x = str(input('"y" to continue (label)'))
			if x.lower() == 'y':
				break
		print('Cheking labels')
		dlc.check_labels(config_path, visualizeindividuals=False)
		break
	#If the user already have a project with labeled data
	elif x.lower() == '2':
		#If the user want to creat a dataset and train the network
		print('Open the config file of the project (config.yaml)')
		config_path = askopenfilename()
		print('Making a dataset for training')
		dlc.create_training_dataset(config_path, augmenter_type='imgaug')
		print('Finished creating dataset.\nBegin training')
		dlc.train_network(config_path, maxiters=100)
		print('Finished train the network.\nBegin evaluate network')
		dlc.evaluate_network(config_path, Shuffles=[1], plotting=True)
		print('Finished evaluate network.\nBegin analyze videos and search for videos')
		current_directory = os.path.dirname(os.path.abspath(__file__))
		list_videos()
		dlc.analyze_videos(config_path, videos_list, save_as_csv=True)
		print('Finished analyze videos\n')
		list_videos()
		dlc.filterpredictions(config_path, videos_list)
		dlc.plot_trajectories(config_path, videos_list)
		break
		#If the user already have a trained network
	elif x.lower() == '3':
		print('Open the config file of the project (config.yaml)')
		config_path = askopenfilename()
		print('Creating a labled video and search for videos')
		current_directory = os.path.dirname(os.path.abspath(__file__))
		list_videos()
		dlc.create_labeled_video(config_path, videos_list, save_frames = True)
		print('Finished creating a labeled video\n')
		break
	elif x.lower() == '4':
		chose_bodyparts = False
		chose_names = True
		current_directory = current_directory+'/'+unique_folder_projects_name('many_projects')
		print('1 = Use one project for example')
		#print('2 = Make all time one project new')
		x = str(input(('Type the number what you want to do: ')))
		if x.lower() == '1':
			number_of_maxiters = []
			number_of_porject = 0
			while True:
				x = input('Write the maxiters numbers with backspace like: "1 50 160" (1 number = 1 project)\n')
				if len(x) == 0:
					print('You write nothing, try again')
				else:
					number_of_maxiters_nit = x.split()
					number_of_porject = len(number_of_maxiters_nit)
					for num in number_of_maxiters_nit:
						try:
							number_nit = int(num)
							number_of_maxiters.append(number_nit)
						except ValueError:
							print(f"Некорректный элемент: {num}. Пропущен.")
					break
			#print('current directoyr1:', current_directory)
			#z = input()
			path_to_lebaled_folder = ''
			print('Creating the projects')
			creat_unique_folder()
			list_videos()
			#print('current directoyr1.1:', current_directory)
			#z = input()
			dlc.create_new_project(project_name, name, videos_list, working_directory=current_directory, copy_videos=True, multianimal=False)
			ask_for_bodyparts()
			print('Ectract frames')
			dlc.extract_frames(config_path, mode='automatic', algo='kmeans', userfeedback=False, crop=False)
			print('Begin labeling.\nPlace the points')
			#dlc.label_frames(config_path)
			#Stops to place the points in napari
			"""
			while True:
				x = str(input('"y" to continue (label)'))
				if x.lower() == 'y':
					break
			"""
			source_folder = os.path.dirname(os.path.abspath(__file__))+'/labeled-data'
			target_folder = current_directory+'/'+folder_name+'/labeled-data'
			if os.path.exists(target_folder):
				shutil.rmtree(target_folder)
			shutil.copytree(source_folder, target_folder)
			print('Cheking labels')
			dlc.check_labels(config_path, visualizeindividuals=False)
			path_to_lebaled_folder = current_directory+'/'+folder_name+'/labeled-data'
			chose_names_dubl = True
			maxiters_number = 0
			#print('number of maxiters:', number_of_maxiters)
			#print('maxiters number:', number_of_maxiters[maxiters_number])
			#x = input()
			y = 0
			while not y == number_of_porject:
				creat_unique_folder()
				#print('current directoyr2:', current_directory)
				#z = input()
				dlc.create_new_project(project_name, name, videos_list, working_directory=current_directory, copy_videos=True, multianimal=False)
				ask_for_bodyparts()
				existing_folder = current_directory+'/'+folder_name+'/labeled-data'
				shutil.rmtree(existing_folder)
				shutil.copytree(path_to_lebaled_folder, existing_folder)
				print('Making a dataset for training')
				dlc.create_training_dataset(config_path, augmenter_type='imgaug')
				print('Finished creating dataset.\nBegin training')
				
				dlc.train_network(config_path, maxiters=int(number_of_maxiters[maxiters_number]))
				print('Finished train the network.\nBegin evaluate network')
				dlc.evaluate_network(config_path, Shuffles=[1], plotting=True)
				print('Finished evaluate network.\nBegin analyze videos and search for videos')
				#current_directory = os.path.dirname(os.path.abspath(__file__))
				dlc.analyze_videos(config_path, videos_list, save_as_csv=True)
				print('Finished analyze videos\n')
				dlc.filterpredictions(config_path, videos_list)
				dlc.plot_trajectories(config_path, videos_list)
				#print('current directoyr2.1:', current_directory)
				#z = input()
				
				y += 1
				maxiters_number += 1
			break

		elif x.lower() == '2':
			break
			chose_names_copys = True
			chose_names_dubl = True
			print('Creating the projects')
			y = 0
			shuffles_number = 1
			while not y == 10:
				creat_unique_folder()
				list_videos()
				dlc.create_new_project(project_name, name, videos_list, working_directory=current_directory, copy_videos=True, multianimal=False)
				ask_for_bodyparts()
				print('Ectract frames')
				dlc.extract_frames(config_path, mode='automatic', algo='kmeans', userfeedback=False, crop=False)
				print('Begin labeling.\nPlace the points')
				dlc.label_frames(config_path)
				#Stops to place the points in napari
				while True:
					x = str(input('"y" to continue (label)'))
					if x.lower() == 'y':
						break
				print('Cheking labels')
				dlc.check_labels(config_path, visualizeindividuals=False)
				print('Making a dataset for training')
				dlc.create_training_dataset(config_path, augmenter_type='imgaug')
				print('Finished creating dataset.\nBegin training')
				dlc.train_network(config_path, maxiters=30000)
				print('Finished train the network.\nBegin evaluate network')
				dlc.evaluate_network(config_path, Shuffles=[1], plotting=True)
				print('Finished evaluate network.\nBegin analyze videos and search for videos')
				current_directory = os.path.dirname(os.path.abspath(__file__))
				dlc.analyze_videos(config_path, videos_list, save_as_csv=True)
				print('Finished analyze videos\n')
				dlc.filterpredictions(config_path, videos_list)
				dlc.plot_trajectories(config_path, videos_list)
				y += 1
				shuffles_number = shuffles_number*10
			break

	elif x.lower() == 'q':
		print('Stoping the code. Bye')
		break

"""
def get_errors(max_iters_list):pass
def myplot(dataframe):pass


dataframe = get_errors([1, 10, 100, 500, 1000])
myplot(dataframe)
"""
