from flask import Flask, render_template, Blueprint, request

from .utils import tile_images

app = Flask(__name__)

grid = (6, 20)

dir = Blueprint('dir', __name__, 
                template_folder= "./templates")

@dir.route('/api/display_dir')
def route_api_display_dir():
    img_dir = request.args['dir']
    returned = False
    while not returned:
        array, returned, results = tile_images(img_dir, grid)
    return results

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8080, debug=True)