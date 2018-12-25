import json
import re

cmd = ""


def decode():
    x1 = cmd[6:-14].split('\' --data \'')
    x2 = x1[0].split('\' -H \'')
    # url
    print('url = "{}"'.format(x2[0]))
    # headers
    headers = {}
    for arg in x2[1:]:
        if not re.match('\S+:\s\S+', arg):
            continue
        hdr = arg.split(': ')
        headers[hdr[0]] = hdr[1]
    print('headers = {}'.format(json.dumps(headers)))
    # params
    if len(x1) < 2:
        return
    params = {}
    for d in x1[1].split('&'):
        y1 = d.split('=')
        params[y1[0]] = y1[1]
    print('params = {}'.format(json.dumps(params)))


if __name__ == '__main__':
    decode()
    print('response = requests.get(url, params=params, headers=headers).text')
