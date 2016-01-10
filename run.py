import requests
import subprocess
import time
import email.utils
import argparse
import sys
from datetime import timedelta


URL_FORMAT = 'https://tools.wmflabs.org/paws/public/{user}/{path}.ipynb?format=code'

lastmodified = None
process = None

argparser = argparse.ArgumentParser()

argparser.add_argument('username')
argparser.add_argument('notebook')
argparser.add_argument('--refresh-interval', default=1, type=int)
args = argparser.parse_args()

while True:
    url = URL_FORMAT.format(user=args.username, path=args.notebook)
    if lastmodified is not None:
        headers = {
            'If-Modified-Since': email.utils.format_datetime(lastmodified + timedelta(seconds=1))
        }
    else:
        headers = {}
    resp = requests.get(url, headers=headers)
    if resp.status_code != 304:
        if process is not None:
            process.kill()
        process = subprocess.Popen([sys.executable, '-c', resp.text])
        lastmodified = email.utils.parsedate_to_datetime(resp.headers.get('last-modified'))
    time.sleep(args.refresh_interval)
