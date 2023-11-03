from flask import Flask, send_from_directory, make_response, abort, render_template, request, send_file
from flask_cors import CORS
from mimetypes import guess_type
import os
import io
from PIL import Image

from dir.app import dir

from utils import display_markdown, serve_pil_image

app = Flask(__name__, static_folder = 'static')
app.register_blueprint(dir)

CORS(app)
shared_folder = 'files'

@app.route('/files', defaults={'path':''}, methods=['GET'])
@app.route('/files/<path:path>')
def route_get_files(path):
    total_path = os.path.join(shared_folder, path)

    if not os.path.exists(total_path):
        return make_response('File doesn\'t exist', 404)
    if os.path.isdir(total_path):
        parent_dir = os.path.dirname(total_path) if path else ''
        parent_dir_text = f'<a href="/{parent_dir}" class="text-dark"><h5><= Go to parent directory</h5></a>' if parent_dir else ''
        return render_template('dir.html', dir=total_path, parent_dir=parent_dir_text)
    
    try:
        mime = guess_type(total_path)[0].split('/')
        #print(mime)
        filetype = mime[0]
        ext = mime[1]

        print(filetype, ext)
    except AttributeError:
        data = open(total_path, 'r').read()
        response = make_response(data, 200)
        response.mimetype = 'text/plain'
        return response

    if filetype == 'text':
        if ext == 'markdown':
            html = display_markdown(total_path)
            return render_template('markdown.html', markdown=html)
        else:
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
    print(path)
    try:
        img = Image.open(total_path)
        dim = (int(dimension[1]), int(dimension[3]))
        size = img.size
        print(size)
        print(dim)
        #multiplier = 1
        multiplier = max(1400/6/size[0]*dim[1], 1400/6/size[1]*dim[0])
        print(multiplier)
        if multiplier < 1:
            compressed_img = img.resize((int(size[0]*multiplier), int(size[1]*multiplier)))
        else:
            compressed_img = img
        img_io = io.BytesIO()
        compressed_img.save(img_io, format='PNG')
        img_io.seek(0)
    except Exception as e:
        print(e)
        return abort(404)#'File is not an image'
    return send_file(img_io, mimetype='image/png')

@app.route('/healthcheck', methods=['GET'])
def healthcheck():
    return {'status':'healthy'}

@app.route('/', methods=['GET'])
def main():
    return render_template('main.html')

if __name__ == '__main__':
    if not os.path.exists(shared_folder):
        os.mkdir(shared_folder)
    #app.run(host="0.0.0.0", port = '8080')
    app.run(host="0.0.0.0", port = '8080', debug=True)