import markdown
import markdown.extensions.mathjax
from io import StringIO
from flask import send_file
import json
import latex


def display_markdown(file_path):
    md = open(file_path, 'r').read()
    html = markdown.markdown(md, extensions=['tables', "codehilite", 'fenced_code', latex])
    return html

def serve_pil_image(pil_img):
    img_io = StringIO()
    pil_img.save(img_io, 'JPEG', quality=70)
    img_io.seek(0)
    return send_file(img_io, mimetype='image/jpeg')



