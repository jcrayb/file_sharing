from flask import Flask, render_template, Blueprint, request, jsonify, abort, make_response
import os
import pandas as pd

from .utils import generateContent
from utils import display_markdown

app = Flask(__name__)

cloud = Blueprint('cloud', __name__, 
                template_folder= "./templates")

shared_folder = 'files'

@cloud.route('/pretty/files', defaults={'path': None})
@cloud.route('/pretty/files/<path:path>')
def userpath(path):
    if not path or os.path.isdir(path):
        return abort(404)

    content, language, full_path = generateContent(path)
    parent_dir = os.path.dirname(os.path.join(shared_folder, path) if path else '')

    filename = os.path.join(shared_folder, path).replace(parent_dir, "").replace('/', '')

    parent_dir_text = f'<a href="/{parent_dir}" class="text-dark text-decoration-none" themed-text><h5 class="text-dark" themed-text><= Go to parent directory</h5></a>' if parent_dir else ''
    if language == 'csv':
        df = pd.read_csv(full_path)
        return render_template('display_sheet.html', raw=os.path.join('/files', path),  table=df.to_html(classes='table table-stripped'), filename=filename, parent_dir=parent_dir_text)
    elif filename[-2:].lower() == 'md':
        print(filename)
        html = display_markdown(full_path)
        return render_template('markdown.html', markdown=html, raw=os.path.join('/files', path), filename=filename, parent_dir=parent_dir_text)
    
    return render_template('display_file.html', content=content, language=language, raw=os.path.join('/files', path), filename=filename, parent_dir=parent_dir_text)
