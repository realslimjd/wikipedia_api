from flask import render_template, url_for
from app import app
import requests

@app.route('/')
@app.route('/index')

def index():
    # Set a new User Agent, per the docs
    # https://www.mediawiki.org/wiki/API:Main_page#Identifying_your_client
    session = requests.Session()
    session.headers.update({'User-Agent': 'JDV New Jersey Image Machine'})

    # Find all the images on the page
    image_titles = []
    returned_json = {}

    endpoint = 'https://en.wikipedia.org/w/api.php'
    params = {'action':'query', 'format':'json', 'prop':'images',
            'titles':'New Jersey'}

    while 'batchcomplete' not in returned_json:
        result = session.get(endpoint, params=params)
        returned_json = result.json()

        # 21648 is the page id
        # How can we make it not a magic number
        for image_attrs in returned_json['query']['pages']['21648']['images']:
            image_titles.append(image_attrs['title'])

        if 'continue' in returned_json:
            params['continue'] = returned_json['continue']['continue']
            params['imcontinue'] = returned_json['continue']['imcontinue']

    # And now get the metadata for each of those images
    image_information = []

    params = {'action':'query', 'format':'json', 'prop':'imageinfo',
                'iiprop':'url|user|userid|canonicaltitle'}

    for image_title in image_titles:
        image_data = {}

        params['titles'] = image_title
        result = session.get(endpoint, params=params)
        returned_json = result.json()

        image_pages = returned_json['query']['pages']
        # from https://stackoverflow.com/questions/3097866/access-an-arbitrary-element-in-a-dictionary-in-python
        # because you can have more than result in the pages dict
        first_page = next(iter(image_pages.values()))
        image_info = first_page['imageinfo'][0]

        # Removes 'File:' from the name
        image_data['name'] = image_info['canonicaltitle'][5:]
        image_data['url'] = image_info['url']
        image_data['user'] = image_info['user']

        image_information.append(image_data)

    return render_template('index.html', images=image_information)
