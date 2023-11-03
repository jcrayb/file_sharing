import markdown
from io import StringIO
from flask import send_file

def display_markdown(file_path):
    md = open(file_path, 'r').read()
    html = markdown.markdown(md,extensions=['tables'])
    return html

def serve_pil_image(pil_img):
    img_io = StringIO()
    pil_img.save(img_io, 'JPEG', quality=70)
    img_io.seek(0)
    return send_file(img_io, mimetype='image/jpeg')
