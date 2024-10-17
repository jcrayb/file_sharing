from flask import Flask, send_from_directory, make_response, abort, render_template, request, send_file, redirect
from flask_cors import CORS
from mimetypes import guess_type
import os
import io
from PIL import Image
import json

from dir.app import dir
from cloud.app import cloud

from utils import display_markdown, isProtected

app = Flask(__name__, static_folder = 'static')
app.register_blueprint(dir)
app.register_blueprint(cloud)

CORS(app)
shared_folder = 'files'
config_folder = 'config'

@app.route('/files', defaults={'path':''}, methods=['GET'])
@app.route('/files/<path:path>')
def route_get_files(path):
    total_path = os.path.join(shared_folder, path)
    parent_dir = os.path.dirname(total_path) if path else ''

    if not os.path.exists(total_path):
        return make_response('File doesn\'t exist', 404)
    
    path = path.split('?')[0]

    if isProtected(path)[0]:
        if request.args.get('password') != isProtected(path)[1]:
            return redirect("/protected/"+path)

    if os.path.isdir(total_path):
        decorative_text = "<= Go to parent directory" if path else "<= Go to main menu"
        parent_dir_text = f'''<a href="/{parent_dir}" class="text-dark text-decoration-none" themed-text>
                                <h5 class="text-dark" themed-text>{decorative_text}</h5></a>'''
        return render_template('dir.html', dir=total_path, parent_dir=parent_dir_text, dirname=total_path.replace(parent_dir, "").replace('/', ''))

    

    try:
        mime = guess_type(total_path)[0].split('/')
        filetype = mime[0]
        ext = mime[1]
    except AttributeError:
        data = open(total_path, 'r').read()
        response = make_response(data, 200)
        response.mimetype = 'text/plain'
        return response

    if filetype == 'text':
        data = open(total_path, 'r').read()
        response = make_response(data, 200)
        response.mimetype = 'text/plain'
        return response
    
    return send_from_directory(shared_folder, path)

@app.route('/compressed/files', defaults={'path':''}, methods=['GET'])
@app.route('/compressed/files/<path:path>')
def route_get_compressed_files(path):
    total_path = os.path.join(shared_folder, path)
    dimension = request.args['dim']
    dim = (int(dimension[1]), int(dimension[3]))

    img = Image.open(total_path)
    size = img.size

    multiplier = max(1400/6/size[0]*dim[1], 1400/6/size[1]*dim[0])

    if multiplier < 1:
        compressed_img = img.resize((int(size[0]*multiplier), int(size[1]*multiplier)))
    else:
        compressed_img = img

    img_io = io.BytesIO()
    compressed_img.save(img_io, format='PNG')
    img_io.seek(0)
    
    return send_file(img_io, mimetype='image/png')

@app.route('/protected', defaults={'path': None})
@app.route('/protected/<path:path>')
def protected(path):
    if isProtected(path)[0] and request.args.get('password') == isProtected(path)[1]:
        return route_get_files(path)
    else:
        error = 'Wrong password' if request.args.get('password') else None

        total_path = os.path.join(shared_folder, path)
        parent_dir = os.path.dirname(total_path) if path else ''
        print(total_path.replace(parent_dir, "").replace('/', ''))
        decorative_text = "<= Go to parent directory" if path else "<= Go to main menu"
        parent_dir_text = f'''<a href="/{parent_dir}" class="text-dark text-decoration-none" themed-text>
                                <h5 class="text-dark" themed-text>{decorative_text}</h5></a>'''
        return render_template('protected.html', dir=total_path, parent_dir=parent_dir_text, dirname=total_path.replace(parent_dir, "").replace('/', ''), error=error, path=path)

@app.route('/healthcheck', methods=['GET'])
def healthcheck():
    return {'status':'healthy'}

@app.route('/', methods=['GET'])
def main():
    return render_template('main.html')

if __name__ == '__main__':
    if not os.path.exists(shared_folder):
        os.mkdir(shared_folder)

    if not os.path.exists(config_folder):
        os.mkdir(config_folder)

    if not os.path.exists('./config/protected-files.json'):
        init = {}
        json.dump(init, open('./config/protected-files.json', 'w'))
    #app.run(host="0.0.0.0", port = '8080')
    app.run(host="0.0.0.0", port = '8080', debug=True)