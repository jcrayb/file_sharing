from flask import Flask, render_template, Blueprint, request, jsonify
import os

from .utils import tile_images, list_folders, is_cached

app = Flask(__name__)

grid = (6, 20)

dir = Blueprint('dir', __name__, 
                template_folder= "./templates")

@dir.route('/api/images')
def route_api_images():
    img_dir = request.args['dir']
    returned = False
    cache = is_cached(img_dir)
    if cache[0]:
        return cache[1]
    while not returned:
        array, returned, results = tile_images(img_dir, grid)
    return results

@dir.route('/api/folders')
def route_api_folders():
    folder_dir = request.args['dir']
    folders = list_folders(folder_dir)
    print(folders)
    return folders

@dir.route('/api/parent_dir')
def route_api_parent_dir():
    folder_dir = request.args['dir']
    folders = os.path.dirname(folder_dir)
    return jsonify(folders)

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8080, debug=True)