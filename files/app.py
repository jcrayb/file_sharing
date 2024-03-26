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
    
    content, language, raw = generateContent(path)
    return render_template('display_file.html', content=content, language=language, raw=raw.replace('\\', '/'), path=path)