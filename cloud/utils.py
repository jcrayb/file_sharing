import os
import mimetypes as mime
import json

cwd = os.path.join(os.getcwd(), 'files')

extDict = {
    'x-python':'python',
    'html':'html',
    'plain':'plaintext',
    'css':'css',
    "json":'json',
    "javascript": "js",
    "markdown": "markdown"
}

def generateContent(path):
    language=''
    props = getFileProps(path)

    if props['type']=='image':
        content = f'<img src="{path}">'
    else:
        if props['ext'] == 'csv':
            return "", 'csv', os.path.join(cwd, path)
        file = open(os.path.join(cwd, path), 'r')
        content = file.read()
        print(props)
        language = extDict[props['ext']] if props['ext'] in extDict else 'plaintext'
        if language == 'json':
            content = json.dumps(json.loads(content), indent=1)
    print(language)
    return content, language, os.path.join(cwd, path), props

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