import os
import json
import codecs

import csv
import shutil
import math

'''
output_csv
'''
def output_csv(output_folder_path, csv_file_name, records, en="utf-8"):
    #make output folder if doesn't exist.
    if os.path.isdir(output_folder_path) is False:
        make_folder(output_folder_path)
    #write csv records
    output_file_path = os.path.join(output_folder_path, csv_file_name)
    with open(output_file_path, "w", encoding=en) as f:
        writer = csv.writer(f, lineterminator="\n")
        writer.writerows(records)
        
'''
get_file_stem
'''
def get_file_stem(file_path):
    file_name = os.path.basename(file_path)
    stem, ext = os.path.splitext(file_name)
    return stem

'''
get_folder_name_list
'''
def get_folder_name_list(parent_folder_path):
    file_list = os.listdir(parent_folder_path)
    folder_name_list = [f for f in file_list if os.path.isdir(os.path.join(parent_folder_path, f))]
    return folder_name_list

'''
save_json
'''
def save_json(save_file_path, dict_data, charset=None, indent_size=4):
    fw = codecs.open(save_file_path,'w', charset)
    json.dump(dict_data,fw,indent=indent_size)
    fw.close()

'''
load_csv_as_list
'''
def load_csv_as_list(load_file_path, line_terminator="\n", charset=''):
    if os.path.isfile(load_file_path) is False:
        print("error : csv file does not exist.")
        print(load_file_path)
        return None
    
    if charset=='':
        csv_file = open(load_file_path, 'r')
    else:
        csv_file = codecs.open(load_file_path, 'r', charset)
    
    loaded_records = None
    loaded_records = csv.reader(csv_file, delimiter=",", doublequote=True, lineterminator=line_terminator, quotechar='"', skipinitialspace=True)
    result = [r for r in loaded_records]
    csv_file.close()

    return result

'''
load_csv_as_dict
'''
def load_csv_as_dict(load_file_path, line_terminator="\n", charset=''):
    if os.path.isfile(load_file_path) is False:
        print("error : csv file does not exist.")
        print(load_file_path)
        return None
    loaded_records = None
    if charset=='':
        csv_file = open(load_file_path, 'r')
        loaded_records = csv.DictReader(csv_file, delimiter=",", doublequote=True, lineterminator=line_terminator, quotechar='"', skipinitialspace=True)
    else:
        csv_file = codecs.open(load_file_path, 'r', charset)
        loaded_records = csv.DictReader(csv_file, delimiter=",", doublequote=True, lineterminator=line_terminator, quotechar='"', skipinitialspace=True)
    
    result = [r for r in loaded_records]
    csv_file.close()
    
    return result

'''
load_json
'''
def load_json(json_file_path,charset=''):
    json_file = None
    if charset=='':
        json_file = open(json_file_path, 'r')
    else:
        json_file  = codecs.open(json_file_path, 'r', charset)
    json_data  = json.load(json_file)
    json_file.close()
    return json_data

'''
put_value_in_range
'''
def put_value_in_range(value, minmax):
    result = value
    if value < minmax[0]:
        result = minmax[0]
    elif value > minmax[1]:
        result = minmax[1]
        
    return result

'''
is_hit
'''
def is_hit(rect_A, rect_B):
    hit = False
    if ((rect_A[0] <= rect_B[2]) and (rect_A[2] >= rect_B[0]) \
        and (rect_A[1] <= rect_B[3]) and (rect_A[3] >= rect_B[1])):
        hit = True
    return hit

'''
is_truncated
'''
def is_truncated(rect_A, rect_B):
    truncated = False
    for i in range(4):
        if rect_A[i]==rect_B[i]:
            truncated = True
            break
    return truncated

'''
make_folder
'''
def make_folder(folder_path):
    if os.path.isdir(folder_path) is False:
        os.makedirs(folder_path)

'''
find_all_file_count
'''
def find_all_folder_info(folder_path, verbose=False, ext=None):
    folder_list = []
    for folder, sub_folder, files in os.walk(folder_path):
        file_count       = 0
        if ext is None:
            file_count = len(files)
        else:
            for file in files:
                file_stem, file_ext  = os.path.splitext(file)
                if file_ext == ext:
                    file_count += 1
        info = {"folder_path":folder, "file_count":file_count}
        folder_list.append(info)
        if verbose==True:
            for folder in folder_list:
                print(folder)
    return folder_list

'''
find_all_folder
'''
def find_all_folder(folder_path, verbose=False):
    folder_list = []
    for folder, sub_folder, files in os.walk(folder_path):
        folder_list.append(folder)
        #for file in files:
            #folder_list.append(os.path.join(folder, file))
    if verbose==True:
        for folder in folder_list:
            print(folder)
    return folder_list

    #compute sin cos
    atan = math.atan2(shift_vec[1], shift_vec[0])
    cos  = math.cos(atan)
    sin  = math.sin(atan)
    last_dx = 0
    last_dy = 0
    last_iou = 0.0
    #shift the position according to shift_vec
    for shift_distance in range(MAX_SHIFT_DISTANCE):
        dx = round(shift_distance*cos)
        dy = round(shift_distance*sin)

'''
get_direction8
'''
def get_direction8(x, y):
    direction = [0,0]
    if x==0 and y==0:
        return direction
    
    atan = math.atan2(y,x)
    deg  = math.degrees(atan)
    if   -180.0 < deg and deg <= -157.5:
        direction = [-1, 0]
    elif -157.5 < deg and deg <= -112.5:
        direction = [-1, 1]
    elif -112.5 < deg and deg <= -67.5:
        direction = [0, 1]
    elif -67.5 < deg and deg <= -22.5:
        direction = [1, 1]
    elif -22.5 < deg and deg <= 22.5:
        direction = [1, 0]
    elif 22.5 < deg and deg <= 67.5:
        direction = [1, -1]
    elif 67.5 < deg and deg <= 112.5:
        direction = [0, -1]
    elif 112.5 < deg and deg <= 157.5:
        direction = [-1, -1]
    elif 157.5 < deg and deg <= 180.0:
        direction = [-1, 0]
        
    return direction