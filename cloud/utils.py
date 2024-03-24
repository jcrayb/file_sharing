import os
import mimetypes as mime

cwd = os.path.join(os.getcwd(), 'files')

extDict = {
    'x-python':'python',
    'html':'html',
    'plain':'plaintext',
    'css':'css'
}

def generateContent(path):
    language=''
    raw=''
    props = getFileProps(path)

    if props['type']=='image':
        content = f'<img src="{path}">'
    elif props['type']=='text' or not props['type']:
        print(os.path.join(cwd, path))
        if props['ext'] == 'csv':
            return "", 'csv', os.path.join(cwd, path)
        file = open(os.path.join(cwd, path), 'r')
        content = file.read()
        language = extDict[props['ext']] if props['ext'] in extDict else 'plaintext'

    return content, language, os.path.join(cwd, path)

def getFileProps(path):
    path = path.replace('\\', '/')
    fileType = mime.guess_type(path)[0]
    
    if fileType:
        type = fileType.split('/')[0]
        ext = fileType.split('/')[1]
    else:
        type= ''
        ext = ''
    print(type, ext)
    return {"type":type, "ext":ext}