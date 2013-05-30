import os

def get_data_files(src_path, dest_path, path):
    '''
    Used for setup.py to grab all of the data_files in a directory
    '''
    file_list = []
    for folder, _, files in os.walk(os.path.join(src_path, path)):
        for filename in files:
            file_data = {}
            file_data['name'] = filename
            file_data['folder'] = folder
            file_data['abspath'] = os.path.join(folder,filename)
            file_list.append(file_data)
    output = {}
    for f in file_list:
        folder = os.path.join(dest_path, f['folder'])
        if folder not in output:
            output[folder] = []
        output[folder].append(f['abspath'])
    data_files = []
    for key, value in output.items():
        data_files.append((key, value))
    return data_files