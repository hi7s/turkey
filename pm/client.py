import codecs
import json
import logging
import re
import uuid

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')

HOST = 'www.domain.com'


def decode_script(src):
    # full url
    full_url = re.findall("http://[^']+", src)[0]
    logging.info('full url: %s', full_url)
    # uri
    uri = full_url.split('?')[0].replace('http://' + HOST, '')
    logging.info(uri)
    # path
    path = uri.split('/')[1:]
    logging.info(path)
    # header
    header = get_header(src)
    # data
    data = get_data(src)
    # query string
    query = get_query(full_url)
    # test point
    event = get_event()
    # method
    method = get_method(src)
    # result
    result = {
        'name': uri,
        'event': event,
        'request': {
            'method': method,
            'header': header,
            'url': {'raw': full_url, 'protocol': 'http', 'host': '{{host}}', 'path': path, 'query': query},
            'body': {'mode': 'raw', 'raw': data},
            'description': {}
        },
        'response': []
    }
    logging.info(result)
    return result


def get_header(src):
    header = []
    for d in re.findall("-H\s'[\w-]+:[^']+'", src):
        result = {}
        kv = d[3:].strip("'").split(': ')
        if kv[0].lower() == 'host':
            result['key'] = kv[0]
            result['value'] = HOST
        elif kv[0].lower() == 'user-agent':
            result['key'] = kv[0]
            result['value'] = '{{ua}}'
        elif kv[0].lower() == 'cookie':
            result['key'] = kv[0]
            result['value'] = '{{cookie}}'
        else:
            result['key'] = kv[0]
            result['value'] = kv[1]
        header.append(result)
    logging.info(header)
    return header


def get_data(src):
    if not re.findall("--data-binary\s'.[^']+'", src):
        return ''
    logging.info(re.findall("--data-binary\s'.[^']+'", src))
    data = re.findall("--data-binary\s'.[^']+'", src)[0][14:].strip("'")
    logging.info(data)
    return data


def get_query(full_url):
    if '?' not in full_url:
        return []
    if not full_url.split('?')[1]:
        return []
    query = []
    for q in full_url.split('?')[1].split('&'):
        qe = q.split('=')
        if qe[0].lower() == '__ts__':
            query.append({'key': qe[0], 'value': '{{$timestamp}}'})
        else:
            query.append({'key': qe[0], 'value': qe[1]})
    logging.info(query)
    return query


def get_event():
    script = {
        'id': str(uuid.uuid4()), 'type': 'text/javascript',
        'exec': [
            'pm.test(\"correct status code\", function () {',
            '    var jsonData = pm.response.json();',
            '    pm.expect(jsonData.code).to.eql(200);',
            '});'
        ]}
    return [{'listen': 'test', 'script': script}]


def get_method(src):
    if re.findall(r'-X\s\w+', src):
        method = re.findall('-X\s\w+', src)[0].split(' ')[1]
    elif re.findall("--data-binary\s'.[^']+'", src):
        method = 'POST'
    else:
        method = 'GET'
    logging.info('method: %s', method)
    return method


if __name__ == '__main__':
    # read scripts(from chrome network monitor)
    f = codecs.open('client.py.in', 'r', 'utf-8')
    scripts = f.readlines()
    f.close()
    # analyse and format
    pm_obj = {
        'info': {
            'schema': 'https://schema.getpostman.com/json/collection/v2.1.0/collection.json',
            'name': HOST
        },
        'item': [decode_script(script) for script in scripts]
    }
    # save to file
    f = codecs.open('client.py.out', 'w', 'utf-8')
    scripts = f.write(json.dumps(pm_obj))
    f.close()
