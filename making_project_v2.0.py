import os
import datetime
from tkinter import Tk
from tkinter.filedialog import askopenfilename
print('Import deeplabcut')
import deeplabcut as dlc  

current_directory = os.path.dirname(os.path.abspath(__file__))
#print(current_directory)
name = 'unknown'
project_name = 'new_project'
date = datetime.date.today()
folder_name = project_name + '-' + name + '-' + str(date)
#print('Имя папки:', folder_name)
suffix = 1
suffax = 0

while True:
	if os.path.exists(os.path.join(current_directory, folder_name)):
		if f'({suffax})' in folder_name:
			project_name = project_name.replace(f'({suffax})', f'({suffix})')
		else:
			project_name = f"{project_name}({suffix})"
		folder_name = project_name + '-' + name + '-' + str(date)
		suffix += 1
		suffax += 1
	elif not os.path.exists(os.path.join(current_directory, folder_name)):
		break

#print('Новое имя: ' + folder_name)
#print('Имя проекта: '+ project_name)
config_path = current_directory+'/'+folder_name+'/config.yaml'

videos_list = []
#print('Сейчас видео:', videos_list)
while True:
	if not os.path.exists(os.path.join(current_directory, 'video')):
		"""Make folder 'video' if there's no folder"""
		os.makedirs(os.path.join(current_directory, 'video'))
		print('Folder "video" has been created at ' + current_directory)
		while True:
			x = str(input('Place the video at the folder and type "y" to continue '))
			if x.lower() == 'y':
				break
	files = os.listdir(os.path.join(current_directory, 'video'))
	while True:
		for filename in files:
			"""Check if the video has a good video type. If yes, it is added to 'videos_list' with the path"""
			if filename.endswith('.mp4') or filename.endswith('.avi'):
				videos_list.append(os.path.join(current_directory, 'video', filename))
		if len(videos_list) == 0:
			"""Check if there are videos in the folder"""
			print('Folder "video" is empty. Please put your videos there')
			str(input('Place the video at the folder and write "y" to continue '))
		else:
			break
	break

#print('Видео Сейчас', videos_list)

while True:
	x = str(input(('Quik strat?(y/n) ')))
	if x.lower() == 'y':
		print('Creat new project')
		dlc.create_new_project(project_name, name, videos_list, working_directory=current_directory, copy_videos=True, multianimal=False)
		print('Chose the config file in:', current_directory+'\\'+folder_name)
		root = Tk()
		root.withdraw()  # Скрываем основное окно
		print("old config path", config_path)
		#config_path = askopenfilename()
		print("new config path", config_path)
		print('Ectract frames')
		dlc.extract_frames(config_path, mode='automatic', algo='kmeans', userfeedback=False, crop=False)
		print('Begin labeling.\nYou can modifed the config file and place the points')
		dlc.label_frames(config_path)
		while True:
			x = str(input('"y" to continue (label)'))
			if x.lower() == 'y':
				break
		print('Cheking labels')
		dlc.check_labels(config_path, visualizeindividuals=False)
		print('Making a dataset for training')
		dlc.create_training_dataset(config_path, augmenter_type='imgaug')
		print('Begin training')
		dlc.train_network(config_path)
		break
	if x.lower() == 'n':
		break