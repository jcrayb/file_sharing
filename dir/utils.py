from PIL import Image
import math
import os
import random
import numpy as np
import time

def tile_size(dim):
    min_var = min(dim)

    width, height = dim

    height /= min_var
    width /= min_var

    height_dec = height - int(height)
    width_dec = width - int(width)
    
    height = math.floor(height)
    width = math.floor(width)
    
    height = math.floor(height) + 1 if height_dec > .5 else height
    width = math.floor(width) + 1 if width_dec > .5 else width


    height = 6 if height > 6 else height
    width = 6 if width > 6 else width
    
    
    return width, height


def get_smallest(dim_list: list) -> int:
    max_dims = []
    for dim in dim_list:
        max_dim = max(dim[0], dim[1])
        max_dims += [max_dim]
    min_value = min(max_dims)
    index = max_dims.index(min_value)
    return index

def list_folders(dir: str) -> list:
    folders = []
    current_path = os.path.join(os.getcwd(), dir)
    #dir = dir.replace('files', '')
    for element in os.listdir(current_path):
        if os.path.isdir(os.path.join(current_path, element)):
            folders += [(element, os.path.join(dir, element))]
    return folders

def tile_images(img_dir: str, grid: tuple) -> np.array:
    results = {'images':{}, 'folders':[], 'files':[]}
    start = time.time()
    img_dims_list = []
    i = 1
    images = os.listdir(img_dir)
    print(images)
    img_list = []
    folders_list = []
    files_list = []
    for image in images:
        img_path = os.path.join(img_dir, image)
        try:
            img = Image.open(img_path)
        except:
            type_ = 'folder' if os.path.isdir(img_path) else 'file' 
            if type_ == 'file':
                
                files_list += [(image, img_path, type_)]
            else:
                print('folder')
                folders_list += [(image, img_path, type_)]
                print(folders_list)
            continue
        print(folders_list)
        img_list += [img_path] 
        size = tile_size(img.size)
        width, height = size

        img_dims_list += [(width, height, i)]
        i+=1
    results['folders'] = folders_list
    results['files'] = files_list
    random.shuffle(img_dims_list)
    #sorted_dims = sorted(img_dims_list, reverse=True)
    #sorted_dims = sorted(sorted_dims, key=lambda x: x[1], reverse=False)
    sorted_dims = img_dims_list
    
    array = [[0 for z in range(grid[0])] for y in range(grid[1])]
    
    array = np.array(array)
    
    i = 0
    j = 0
    z = 0
    
    while len(sorted_dims) >0:
        if time.time()-start>0.2:
            return array, False, results
            
        for dims in sorted_dims:
            height = dims[1]
            width = dims[0]
            index = dims[2]
            
            if i+width < 7:
    
                if height == 1:
                    if array[j, i:i+width].any():
                        z += 1
                        continue
                    array[j, i:i+width] = [index for z in range(width)]
                    results['images'][index] = {'link':img_list[index-1], 'position':[j, i], 'size':[height, width]}
                else:
                    if array[j:j+height, i].any():
                        z += 1
                        continue
                    array[j:j+height, i] = [index for z in range(height)]
                    results['images'][index] = {'link':img_list[index-1], 'position':[j, i], 'size':[height, width]}
                i = i+width
                if i == 6:
                    i = 0 
                    j += 1
                z = 0 
                sorted_dims.remove(dims)
                break
        if z >= len(sorted_dims) and len(sorted_dims):
            if not array[j, i].any():
                
                smol_index = get_smallest(sorted_dims)
                array[j, i] = sorted_dims[smol_index][2]
                sorted_dims.remove(sorted_dims[smol_index])
                print(f'forcing inserts, index = {smol_index}')
                results['images'][index] = {'link':images[index-1], 'position':[j, i], 'size':[1, 1]}
            else:
                i += 1
                if i == 6:
                    i = 0 
                    j += 1
                z=0
                continue
                
            z = 0
            i += 1
            if i == 6:
                i = 0 
                j += 1
    return array, True, results