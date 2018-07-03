''''
Gets the name, url, and user associated with all the images on the NJ wikipedia page
'''
import argparse
import requests

# API Documentation
# https://en.wikipedia.org/w/api.php?action=help&modules=query%2Bimages
# https://en.wikipedia.org/w/api.php?action=help&modules=query%2Bimageinfo

def find_images_on_page(session, debug=False):
    '''
    Returns a list of image titles.

    This pulls from the Wikipedia API. It continue polling the API until
    'batcomplete' is returned, signifying there are no more results
    '''
    image_titles = []
    returned_json = {}

    endpoint = 'https://en.wikipedia.org/w/api.php'
    params = {'action':'query', 'format':'json', 'prop':'images',
            'titles':'New Jersey'}

    while 'batchcomplete' not in returned_json:
        result = session.get(endpoint, params=params)
        returned_json = result.json()

        if debug:
            print(returned_json)

        # 21648 is the page id
        # How can we make it not a magic number
        for image_attrs in returned_json['query']['pages']['21648']['images']:
            if debug:
                print(image_attrs)
            image_titles.append(image_attrs['title'])

        if 'continue' in returned_json:
            params['continue'] = returned_json['continue']['continue']
            params['imcontinue'] = returned_json['continue']['imcontinue']

    if debug:
        print(image_titles)

    return image_titles


# This could be threaded
def get_image_metadata(session, image_names, debug=False):
    '''
    Returns a dict of dicts, where each key is the name of the image.
    Each image contains a url, which is the actual url of the image, and a
    user, which is the user who uploaded the image
    '''
    image_information = []

    endpoint = 'https://en.wikipedia.org/w/api.php'
    params = {'action':'query', 'format':'json', 'prop':'imageinfo',
                'iiprop':'url|user|userid|canonicaltitle'}

    for image_name in image_names:
        image_data = {}

        params['titles'] = image_name
        result = session.get(endpoint, params=params)
        returned_json = result.json()

        if debug:
            print('\n{0}'.format(returned_json))

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

    if debug:
        for image in image_information:
            print('User {0} provided image {1} at {2}'.format(image['user'],
                image['name'], image['url']))

    return image_information


def main():
    '''
    Creates a session to handle API requests, and then runs two functions
    One gets all the image names, the other gets all the metadata
    '''
    parser = argparse.ArgumentParser(
        prog='James\'s Amazing Wikipedia Image Downloader',
        description='Get some images from Wikipedia')

    parser.add_argument('-d', '--debug', dest='debug', action='store_true')

    args = parser.parse_args()

    debug = args.debug

    # Set a new User Agent, per the docs
    # https://www.mediawiki.org/wiki/API:Main_page#Identifying_your_client
    session = requests.Session()
    session.headers.update({'User-Agent': 'JDV New Jersey Image Machine'})

    image_titles = find_images_on_page(session, debug=debug)
    image_metadata = get_image_metadata(session, image_titles, debug=debug)

    return image_metadata


if __name__ == '__main__':
    main()
