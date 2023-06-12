#Old version
import os
import datetime
import re
import deeplabcut as dlc    

quick_start = True
current_directory = os.path.dirname(os.path.abspath(__file__))
"""Cherche the current directory"""

def list_videos2(current_directory):
    """Looks in the folder 'video' and save there name and path"""
    videos_list = []
    if not os.path.exists(os.path.join(current_directory, 'video')):
        """Make folder 'video' if there's no folder"""
        os.makedirs(os.path.join(current_directory, 'video'))
        print('Folder "video" has been created at ' + current_directory)
        return []
    files = os.listdir(os.path.join(current_directory, 'video'))
    for filename in files:
        """Check if the video has a good video type. If yes, it is added to 'videos_list' with the path"""
        if filename.endswith('.mp4') or filename.endswith('.avi'):
            videos_list.append(os.path.join(current_directory, 'video', filename))
    if len(videos_list) == 0:
        """Check if there are videos in the folder"""
        print('Folder "video" is empty. Please put your videos there')
    return videos_list
def generate_unique_folder_name(project_nameL, name, date):
    """Generate unique name for the folder"""
    folder_name = project_nameL + '-' + name + '-' + str(date)
    if not os.path.exists(os.path.join(current_directory, folder_name)):
        """If there is no folder with the same name, return the name"""
        print('There is not a folder with the same name')
        return folder_name
    suffix = 1
    start = project_nameL.find('(')
    end = project_nameL.find(')')
    digit = ''
    global project_name
    if start != -1 and end != -1:
        digit = project_name[start+1:end]
    if digit.isdigit():
        number = int(digit)
        suffix += number
        print('Yesys')
    else:
        print("Npnno")
    print('There is a folder with the same name')
    while True:
        """Generate numbers while the folders have the same name"""
        project_name = f"{project_nameL}({suffix})"
        new_folder_name = f"{project_name}-{name}-{date}"
        print('Новое имя: ' + new_folder_name)
        while True:
            x = str(input('"y" to continue (unique)'))
            if x.lower() == 'y':
                break
        if not os.path.exists(os.path.join(current_directory, new_folder_name)):
            """If the folder name is unique, return it"""
            return new_folder_name

def project_creat():
    """Creat new project"""
    date = datetime.date.today()
    """Takes the date"""
    global project_name, name
    if quick_start == False:
        """If the user chose "not quick start", he have to write the name"""
        project_name = str(input('Name of the project: '))
        name = str(input('Name of the experimenter: '))
    else:
        """If the user chose "quick start", all will be automatic"""
        project_name = 'new_project'
        name = 'unknown'
    global project_folder, config_path
    project_folder = generate_unique_folder_name(project_name, name, str(date))
    print('eeeeEEEeee', project_name)
    config_path = os.path.join(current_directory, project_folder, 'config.yaml')
    """Sets two import things and make it global"""
    print(list_videos2(current_directory))
    print('Creating new project')
    dlc.create_new_project(project_name, name, list_videos2(current_directory), working_directory=current_directory, copy_videos=True, multianimal=False)
    while True:
        x = str(input('"y" to continue (new project)'))
        if x.lower() == 'y':
            break
    """Create a new project"""
    print('Project has been maked! The folder name is: '+project_folder+'\nThe directory of the project: '+current_directory+'\\'+project_folder)
def frames_extract():
    """Extract the frames"""
    print('Ectract frames')
    dlc.extract_frames(config_path, mode='automatic', algo='kmeans', userfeedback=False, crop=False)
    print('Succes extracted')
def frames_label():
    """Label the frames"""
    print('Begin labeling')
    dlc.label_frames(config_path)
    #napari
    while True:
        x = str(input('"y" to continue (label)'))
        if x.lower() == 'y':
            break
    print('Succes full labeled\nCheking it')
    dlc.check_labels(config_path, visualizeindividuals=False)
    print('Succes checked')
def dataset_training_create():
    """Create a dataset for trainig"""
    print('Making a dataset for training')
    dlc.create_training_dataset(config_path, augmenter_type='imgaug')
    print('Succes created')
def train_network():
    """Train the network"""
    print('Begin training')
    dlc.train_network(config_path)
    print('Succes full trained')

while True:
    """Asking how the user will start the code (unly quik now)"""
    x = str(input('Quick start? y/n '))
    if x.lower() == 'y':
        """If yes, it will do all the function"""
        quick_start = True
        print('Starting the quik mode')
        project_creat()
        frames_extract()
        frames_label()
        #dataset_training_create()
        #train_network()
        break
    else:
        """If the symbol is not correct"""
        print("There's not this symbol")


"""The part of the code for "not quick". Doesn't work now """
"""
print('Create new project or use the exist one?')

while True:
    x = str(input('new/load\n'))
    if x == 'new':
        print('Project created')
        #project_creat()
        break
    elif x == 'load':
        print('Chose the project:')
        break"""

"""
    elif x.lower() == 'n':
        quick_start = False
        print('Запуск детального старта')
        # Список доступных функций
        available_functions = [project_creat, frames_extract, frames_label, dataset_training_create, train_network]
        while available_functions:
            # Предлагаем выбрать функцию для выполнения
            print("Выберите функцию для выполнения:")
            for i, func in enumerate(available_functions):
                print(f"{i+1}. {func.__name__}")

            # Получаем выбор пользователя
            choice = input("Введите номер функции: ")

            # Проверяем валидность выбора
            if not choice.isdigit() or int(choice) < 1 or int(choice) > len(available_functions):
                print("Некорректный выбор. Попробуйте снова.")
                continue

            # Получаем индекс выбранной функции
            index = int(choice) - 1

            # Выполняем выбранную функцию
            selected_function = available_functions[index]
            selected_function()

            # Удаляем выполненную функцию из списка доступных функций
            available_functions.pop(index)

            # Проверяем, остались ли еще доступные функции
            if not available_functions:
                print("Выполнены все доступные функции.")
            else:
                print("Продолжить выполнение другой функции? (y/n)")
                response = input()
                if response.lower() != 'y':
                    break
"""
#New version