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


    height = 4 if height > 4 else height
    width = 4 if width > 4 else width
    
    
    return width, height


def get_smallest(dim_list: list) -> int:
    max_dims = []
    for dim in dim_list:
        max_dim = max(dim[0], dim[1])
        max_dims += [max_dim]
    min_value = min(max_dims)
    index = max_dims.index(min_value)
    return index
    
def tile_images(img_dir: str, grid: tuple) -> np.array:
    results = {}
    start = time.time()
    img_dims_list = []

    i = 1
    images = os.listdir(img_dir)
    img_list = []
    for image in images:
        img_path = os.path.join(img_dir, image)
        if os.path.isdir(img_path):
            continue
        img_list += [img_path] 
        img = Image.open(img_path)
        size = tile_size(img.size)
        width, height = size
        
        img_dims_list += [(width, height, i)]
        i+=1
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
                    results[index] = {'link':img_list[index-1], 'position':[j, i], 'size':[height, width]}
                else:
                    if array[j:j+height, i].any():
                        z += 1
                        continue
                    array[j:j+height, i] = [index for z in range(height)]
                    results[index] = {'link':img_list[index-1], 'position':[j, i], 'size':[height, width]}
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
                results[index] = {'link':images[index-1], 'position':[j, i], 'size':[1, 1]}
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