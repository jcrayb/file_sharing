from flask import Flask, render_template, Blueprint, request, jsonify, abort, make_response, redirect
import os
import pandas as pd

from .utils import generateContent, isProtected
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

    
    if path[-3:].lower() == 'pdf':
        print(path)
        return redirect('/'+os.path.join(shared_folder, path))
    
    content, language, full_path = generateContent(path)
    parent_dir = os.path.dirname(os.path.join(shared_folder, path) if path else '')
    path = path.split('?')[0]

    if isProtected(path)[0]:
        if request.args.get('password') != isProtected(path)[1]:
            return redirect("/pretty/protected/"+path)

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


@cloud.route('/pretty/protected', defaults={'path': None})
@cloud.route('/pretty/protected/<path:path>')
def protected(path):
    if isProtected(path)[0] and request.args.get('password') == isProtected(path)[1]:
        return userpath(path)
    else:
        error = 'Wrong password' if request.args.get('password') else None
        return render_template('protected.html', path=path, error=error)