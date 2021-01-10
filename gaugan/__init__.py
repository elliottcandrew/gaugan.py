import requests
import re
import base64
import random
import string
import http.client
import imghdr


# url is something like http://12.34.56.78:443/
# changes periodically
# used for sending map and receiving image
def getUrl():
    r = requests.get('http://34.216.122.111/gaugan/demo.js')
    urls = re.findall(
        r'\'(http.*?://.*?/)\'', re.search(r'urls=.*?;', r.text)[0])
    return urls[0]


def segmentImage(image, url=None):
    if not isinstance(image, bytes):
        raise(ValueError('Image must be bytes.'))

    if url is None:
        url = getUrl()

    # generate name for requests
    name = ''.join(random.choices(string.ascii_lowercase + string.digits, k=20))

    data = {'name': name}
    files = [
        ('file', (name + '.png', image, 'image/png'))
    ]

    requests.post(url + 'nvidia_gaugan_submit_real_image', data=data, files=files)

    r = requests.post(url + 'nvidia_gaugan_return_segmap', stream=True, data=data)

    if r.status_code != 200:
        # print(r.status_code)
        raise(RuntimeError(f'{http.client.responses[r.status_code]} ({r.status_code}) while processing image.'))

    r.raw.decode_content = True
    return r.raw.data


def processImage(image, style='random', url=None):
    if not isinstance(image, bytes):
        raise(ValueError('Image must be bytes.'))

    if imghdr.what(None, image) != 'png':
        raise(ValueError('Image must be PNG format.'))

    if not isinstance(style, int) and style != 'random':
        raise(ValueError('Wrong style, must be an integer or \'random\''))

    if url is None:
        url = getUrl()

    # get b64 encoded image
    imgb64 = 'data:image/png;base64,' + str(base64.b64encode(image))[2:-1]

    # generate name for requests
    name = ''.join(random.choices(string.ascii_lowercase + string.digits, k=20))

    # send map img to server
    requests.post(url + 'nvidia_gaugan_submit_map', data={
        'imageBase64': imgb64,
        'name': name
    })
    # print(g.request.body)

    # get generated img from server
    r = requests.post(url + 'nvidia_gaugan_receive_image', stream=True, data={
        'name': name,
        'style_name': str(style)
    })

    # print(r.text)

    if r.status_code != 200:
        raise(RuntimeError(f'{http.client.responses[r.status_code]} ({r.status_code}) while processing image.'))

    r.raw.decode_content = True
    return r.raw.data
