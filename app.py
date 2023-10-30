from flask import Flask, send_from_directory, make_response, abort, render_template
from flask_cors import CORS
from mimetypes import guess_type
import os

from dir.app import dir

#from utils import display_markdown

app = Flask(__name__, static_folder = 'static')
app.register_blueprint(dir)

CORS(app)
shared_folder = 'files'

@app.route('/files', defaults={'path':''}, methods=['GET'])
@app.route('/files/<path:path>')
def route_get_files(path):
    if not path:
        return abort(404)
    

    total_path = os.path.join(shared_folder, path)

    if not os.path.exists(total_path):
        return make_response('File doesn\'t exist', 404)
    if os.path.isdir(total_path):
        return render_template('dir.html', dir=total_path)
    
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
        '''if ext == 'markdown':
            html = display_markdown(total_path)
            return render_template('markdown.html', markdown=html)'''
        #else:
        data = open(total_path, 'r').read()
        response = make_response(data, 200)
        response.mimetype = 'text/plain'
        return response
    
    return send_from_directory(shared_folder, path)

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