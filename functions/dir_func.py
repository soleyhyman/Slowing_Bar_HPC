# make necissary dirs
import os
import glob
from datetime import datetime

def find_input_file(dir,type):
    pattern=os.path.join(dir,type)
    files=glob.glob(pattern)
    if files:
        file_name = os.path.basename(files[0])
        print(f'Using: {file_name} as file')
        return file_name
    else:
        print('No File Found')
        return -1

def get_current_time_dhm():
    now = datetime.now()
    
    # Calculate total days since the beginning of the year
    start_of_year = datetime(now.year, 1, 1)
    days = (now - start_of_year).days
    
    # Get hours and minutes
    hours = now.hour
    minutes =now.minute
    
    return f"{days}.{hours}.{minutes}"

def create_directories(path):
    os.makedirs(path, exist_ok=True)

def get_unique_filename(base_name, extension, directory):
    counter = 1
    filename = os.path.join(directory, f"{base_name}.{extension}")
    while os.path.exists(filename):
        filename = os.path.join(directory, f"{base_name}{counter}.{extension}")
        counter += 1
    return filename

# this function is intended to take a dictionary and return two 
#       dictionaries one of the serializable objs and one of non-serializable
def json_serialize_check(input_dict):
    # sets initial dicts
    serializable={}
    non_serial={}
    json_serializable_types = {
    "<class 'str'>": True,
    "<class 'int'>": True,
    "<class 'float'>": True,
    "<class 'bool'>": True,
    "<class 'NoneType'>": True,
    }

    # iterate over the dicts values and if its a dict run for the dict,
    #   if its json serializable add to serializable
    #   if its not add to non_serial
    for key,value in input_dict.items():
        if type(value) is dict:
            ser,nser=json_serialize_check(value)
            serializable[key]=ser
            non_serial[key]=nser
        elif type(value) is list:
            lit_clean,lit_dirty=json_serialize_list(value)
            serializable[key]=lit_clean
            non_serial[key]=lit_dirty
        elif json_serializable_types.get(str(type(value)),False):
            serializable[key]=value
        else:
            non_serial[key]=value
    return serializable, non_serial

# takes in a list and returns two lists, one clean for json one dirty
def json_serialize_list(input_list):
    json_serializable_types = {
    "<class 'str'>": True,
    "<class 'int'>": True,
    "<class 'float'>": True,
    "<class 'bool'>": True,
    "<class 'NoneType'>": True,
    }
    output_clean=[]
    output_dirty=[]
    if len(repr(input_list))>len(str(input_list)):
        return repr(input_list),[]
    else:
        for item in input_list:
            if type(item) is dict:
                dict_clean,dict_dirty=json_serialize_check(item)
                output_clean.append(dict_clean)
                output_dirty.append(dict_dirty)
            elif type(item) is list:
                lit_clean,lit_dirty=json_serialize_list(item)
                output_clean.append(lit_clean)
                output_dirty.append(lit_dirty)
            elif json_serializable_types.get(str(type(item)),False):
                output_clean.append(item)
            else:
                output_dirty.append(item)
        return output_clean,output_dirty
# this function takes two dicts, one of a json clean and one of a json dirty
#   it the goes over json dirty to see if some vars are readable from print 
#   and appends these to json clean

def json_dirty_to_clean(js_clean,js_dirty):
    keys=[]
    # Iterates over js_dirty and cleans them while attaching cleaned keys to keys[]
    for key,value in js_dirty.items():
        if type(value) is dict:
            sub_clean,sub_dirty=json_dirty_to_clean({},value)
            js_clean[key]=sub_clean
            js_dirty[key]=sub_dirty
        elif type(value) is list:
            ls_clean,ls_dirty=json_dirty_to_clean_list(value)
            js_clean[key].extend(ls_clean)
            js_dirty[key]=ls_dirty
        else:
            js_clean[key]=str(value)
            keys.append(key)

    # iterates over appended keys and removes them from js_dirty    
    for key in keys:
        js_dirty.pop(key)

    return js_clean,js_dirty

def json_dirty_to_clean_list(js_ls_dirty):
    indexs=[]
    cleaned=[]
    dirty=[]
    if len(repr(js_ls_dirty))<len(str(js_ls_dirty)):
        return repr(js_ls_dirty),[]
    else:
        for item in js_ls_dirty:
            if type(item) is dict:
                cl_dict,dt_dict=json_dirty_to_clean({},item)
                cleaned.append(cl_dict)
                dirty.append(dt_dict)
            elif type(item) is list:
                sub_ls_clean,sub_ls_dirty=json_dirty_to_clean_list(item)
                cleaned.append(sub_ls_clean)
                dirty.append(sub_ls_dirty)
            else:
                cleaned.append(repr(item))
        return cleaned,dirty

def json_serialize_full(input_dict):
    clean,dirty=json_serialize_check(input_dict)
    clean1,dirty1=json_dirty_to_clean(clean,dirty)
    return clean1,dirty1
