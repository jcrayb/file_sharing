from flask import Flask, render_template, Blueprint, request, jsonify, abort
import os

from .utils import generateContent

app = Flask(__name__)

cloud = Blueprint('cloud', __name__, 
                template_folder= "./templates")

@cloud.route('/pretty/files', defaults={'path': None})
@cloud.route('/pretty/files/<path:path>')
def userpath(path):
    if not path or os.path.isdir(path):
        return abort(404)
    '''if not dbFileExists(path):
        return jsonify('error'), 404

    print(dbGetFileProps(path))
    if dbGetFileProps(path)['name'].split('.')[-1] == 'csv':
        df = pd.read_csv(path)
        return render_template('display_sheet.html', path=path, table=df.to_html(classes='table table-stripped'))'''
    content, language, raw = generateContent(path)
    return render_template('display_file.html', content=content, language=language, raw=raw.replace('\\', '/'), path=path)