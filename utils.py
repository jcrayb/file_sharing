import markdown

def display_markdown(file_path):
    md = open(file_path, 'r').read()
    html = markdown.markdown(md,extensions=['tables'])
    return html