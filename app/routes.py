from app import app
from app import api_test

@app.route('/')
@app.route('/index')


def create_img_html(image_data):
    html = '''
<div class="imgblock">
    <div class="img-title">''' + image_data['name'] + '''</div>
    <img src="''' + image_data['url'] + '''">
    <div class="img-user">Via user:''' + image_data['user'] + '''</div>
</div>'''
    return html

def index():

    nj_images = api_test.main()

    html_document = '''
<html>
<head>
    <title>James's W2O Application</title>
    <link rel="stylesheet" type="text/css" href="nj_wiki.css">
</head>
<body>
    '''

    for image in nj_images:
        html_document += create_img_html(image)

    html_document += '''
</body>
</html>
'''
    return   