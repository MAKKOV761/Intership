import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from tkinter import Tk
from tkinter.filedialog import askdirectory


root = Tk()
root.withdraw()
directory = askdirectory(title="Chose the folder with the projects")

def find_csv_files(directory):
    csv_files = []  # Список для хранения найденных файлов CSV
    
    # Путь к папке evaluation-results
    evaluation_results_dir = os.path.join(directory, "evaluation-results")
    
    # Проверка наличия папки evaluation-results
    if not os.path.exists(evaluation_results_dir):
        print("Folder 'evaluation-results' не найдена.")
        return csv_files
    
    # Обход всех файлов внутри папки evaluation-results
    for root, dirs, files in os.walk(evaluation_results_dir):
        for file in files:
            if file.endswith(".csv"):
                csv_file = os.path.join(root, file)
                csv_files.append(csv_file)
    
    return csv_files
csv_files = find_csv_files(directory)

# Списки для хранения значений
training_iterations = []
train_error = []
test_error = []
train_error_with_p_cutoff = []
test_error_with_p_cutoff = []

# Цикл по файлам CSV
for file in csv_files:
	file_path = os.path.join(directory, file)
	
	# Чтение CSV файла и извлечение значений
	df = pd.read_csv(file_path)
	
	# Извлечение значений по названиям столбцов
	training_iterations.append(df.loc[0, 'Training iterations:'])
	train_error.append(df.loc[0, ' Train error(px)'])
	test_error.append(df.loc[0, ' Test error(px)'])
	train_error_with_p_cutoff.append(df.loc[0, 'Train error with p-cutoff'])
	test_error_with_p_cutoff.append(df.loc[0, 'Test error with p-cutoff'])

# Сортировка значений
training_iterations = np.sort(training_iterations)
train_error = np.sort(train_error)
test_error = np.sort(test_error)
train_error_with_p_cutoff = np.sort(train_error_with_p_cutoff)
test_error_with_p_cutoff = np.sort(test_error_with_p_cutoff)

# Вывод результатов
print("Training iterations:", training_iterations)
print("Train error(px):", train_error)
print("Test error(px):", test_error)
print("Train error with p-cutoff:", train_error_with_p_cutoff)
print("Test error with p-cutoff:", test_error_with_p_cutoff)

fig, ax = plt.subplots()
"""
numbers = [0, 2000, 4000, 6000, 8000, 10000]
Train_error = [6.32, 5.98, 4.23, 3.45, 2.21, 1.75]
Test_error = [6.25, 5.85, 4.34, 3.49, 2.76, 1.21]
Train_error_with_pcutoff = [6.32, 5.98, 4.23, 3.45, 2.21, 1.75]
Test_error_with_pcutoff = [6.25, 5.85, 4.34, 3.49, 2.76, 1.21]
"""
ax.plot(training_iterations, train_error, marker='o', color='b', label='Train error')
ax.plot(training_iterations, test_error, marker='o', color='r', label='Test error')
ax.plot(training_iterations, train_error_with_p_cutoff, marker='o', color='g', label='Train error with p-cutoff')
ax.plot(training_iterations, test_error_with_p_cutoff, marker='o', color='y', label='Test error with p-cutoff')

ax.legend(loc='lower left')

plt.show()