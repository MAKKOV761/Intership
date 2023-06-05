import deeplabcut as dlc
#C:/Users/Admin/Desktop/Newfortest/trainig_model-Victor-2023-06-02
x=str(input('Path to the PROJECT: '))
print('\n')

with open('config.yaml', 'r+') as file:
    lines = file.readlines()
    target_line_index = 8
    current_line = lines[target_line_index]
    modified_line = current_line.split(":")[0] + ": " + x + "\n"
    lines[target_line_index] = modified_line
    file.seek(0)
    file.writelines(lines)
    file.truncate()
dlc.train_network(x + '/config.yaml')