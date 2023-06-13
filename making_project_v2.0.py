import os
import datetime
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import subprocess
import sys
print('Import deeplabcut')
import deeplabcut as dlc  

def creat_unique_folder():
	global current_directory, name, project_name, date, folder_name
	current_directory = os.path.dirname(os.path.abspath(__file__))
	#print(current_directory)
	name = 'unknown'
	project_name = 'new_project'
	date = datetime.date.today()
	folder_name = project_name + '-' + name + '-' + str(date)
	print('Имя папки:', folder_name)
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
			global config_path
			config_path = current_directory+'/'+folder_name+'/config.yaml'
			break

#print('Новое имя: ' + folder_name)
#print('Имя проекта: '+ project_name)

#print('Сейчас видео:', videos_list)
def list_videos():
	global videos_list
	videos_list = []
	suffix = 1
	suffax = 0
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
root = Tk()
root.withdraw()  # Скрываем основное окно

while True:
	x = str(input(('Not labeled?(y/n) ')))
	if x.lower() == 'y':
		creat_unique_folder()
		list_videos()
		print('Creat new project')
		dlc.create_new_project(project_name, name, videos_list, working_directory=current_directory, copy_videos=True, multianimal=False)
		if sys.platform.startswith('darwin'):
		    # Открыть файл в стандартном текстовом редакторе на macOS
		    subprocess.run(["open", "-t", config_path])
		elif sys.platform.startswith('win'):
		    # Открыть файл в стандартном текстовом редакторе на Windows
		    subprocess.run(["notepad", config_path])
		elif sys.platform.startswith('linux'):
		    # Открыть файл в стандартном текстовом редакторе на Linux
		    subprocess.run(["xdg-open", config_path])
		else:
		    print("Неизвестная операционная система.")
		while True:
			x = str(input('"y" to continue (config file modified)'))
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
		while True:
			x = str(input('"y" to continue (label)'))
			if x.lower() == 'y':
				break
		print('Cheking labels')
		dlc.check_labels(config_path, visualizeindividuals=False)
		break
	if x.lower() == 'n':
		config_path = askopenfilename()
		print('Making a dataset for training')
		dlc.create_training_dataset(config_path, augmenter_type='imgaug')
		print('Begin training')
		dlc.train_network(config_path)
		break