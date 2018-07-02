''''
Let's see what data coming from the Wikipedia API looks like
'''
import argparse
import requests

# API Documentation
# https://en.wikipedia.org/w/api.php?action=help&modules=query%2Bimages
# https://en.wikipedia.org/w/api.php?action=help&modules=query%2Bpageimages

def get_images(debug=False):
    '''
    '''
    image_names = []
    returned_json = {}

    endpoint = 'https://en.wikipedia.org/w/api.php'
    params = {'action':'query', 'format':'json', 'prop':'images',
            'titles':'New Jersey'}

    while 'batchcomplete' not in returned_json:

        r = requests.get(endpoint, params)

        returned_json = r.json()

        if debug:
            print(returned_json)

        # 21648 is the page id
        # How can we make it not a magic number
        for image_name in returned_json['query']['pages']['21648']['images']:
            if debug:
                print(image_name)
            image_names.append(image_name)

        if 'continue' in returned_json:
            params['continue'] = returned_json['continue']['continue']
            params['imcontinue'] = returned_json['continue']['imcontinue']

    if debug:
        print(image_names)


def main():
    '''
    '''
    parser = argparse.ArgumentParser(
        prog='James\'s Amazing Wikipedia Image Downloader',
        description='Get some images from Wikipedia')

    parser.add_argument('-d', '--debug', dest='debug', action='store_true')

    args = parser.parse_args()

    debug = args.debug

    get_images(debug=debug)


if __name__ == '__main__':
    main()
