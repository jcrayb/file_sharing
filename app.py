from flask import Flask, send_from_directory, make_response, abort
from flask_cors import CORS
from mimetypes import guess_type
import os

app = Flask(__name__, static_folder = 'static')
CORS(app)
shared_folder = 'files'


@app.route('/files', defaults={'path':''}, methods=['GET'])
@app.route('/files/<path:path>')
def route_get_files(path):
    total_path = os.path.join(shared_folder, path)

    if not os.path.exists(total_path):
        return make_response('File doesn\'t exist', 404)
    
    mime = guess_type(total_path)[0].split('/')
    filetype = mime[0]
    ext = mime[1]

    if filetype == 'text':
        data = open(total_path, 'r').read()
        response = make_response(data, 200)
        response.mimetype = 'text/plain'
        return response
    
    return send_from_directory(shared_folder, path)

@app.route('/healthcheck')
def healthcheck():
    return {'status':'healthy'}

if __name__ == '__main__':
    if not os.path.exists(shared_folder):
        os.mkdir(shared_folder)
    app.run(host="0.0.0.0", port = '8080')
    #app.run(host="0.0.0.0", port = '8080', debug=True)