#!/usr/bin/env python3
import sys
import json
import os
import requests
import random
from urllib.parse import quote
from urllib.request import urlretrieve
import webbrowser


CRX_DIR = 'extensions'
CEM_FILE = 'Cemfile'


def get_crx_path(uid: str, directory: str) -> str:
    """Return the local crx path for an extension

    :param uid: crx unique identifier
    :param directory: local directory
    :return: local crx path
    """
    return os.path.join(directory, f'{uid}.crx')


def open_window(uid: str) -> bool:
    """Open browser window to install extensions

    Workaround until installing extensions automatically works.

    :param uid: crx unique ifentifier
    :return: true if browser window is opened
    """
    url = f'https://chrome.google.com/webstore/detail/{uid}'
    # chrome_path = '/usr/bin/chromium-browser'
    # chrome_path = '/usr/bin/chromium-browser --profile-directory="Profile 1" %s'
    # webbrowser.get(chrome_path).open(url)
    webbrowser.get().open(url)
    return True


def download(uid: str, file_path: str) -> bool:
    """Download the crx using the crx uid

    :param uid: crx unique identifier
    :param file_path: to save the crx file to
    :return: true if the file is downloaded
    """
    url = 'https://clients2.google.com/service/update2/crx'
    url += '?response=redirect&prodversion=49.0&x='
    url += f'id={uid}'
    #url += '%26installsource%3Dondemand%26uc'
    url += quote('&installsource=ondemand&uc')
    urlretrieve(url, file_path)
    return os.path.exists(file_path)


def deobfuscate_output(text: str) -> dict:
    """Deobfuscate extension output.

    Oddity needed to read google's obfuscation of their json into array:
    1. Skips the first 4 chars
    2. Removes new lines which returns json
    3. Gets the first array value
    4. Within that array value, get its second value
    5. Within that array value, get its second value

    :param text: returned from google's end point
    :return: correct json dictionary
    """
    return json.loads(text[4:].replace('\n', ''))[0][1][1]


def search(text: str) -> dict:
    """Search for extensions

    :param text: search term
    :return: dictionary of extensions
    """
    headers = {
        'origin': 'https//chrome.google.com',
        'accept-language': 'en-US,en;q=0.9',
        'accept-encoding': 'gzip, deflate, br',
        'accept': '*/*',
        'referer': 'https//chrome.google.com/',
        'content-type': 'application/x-www-form-urlencoded;charset=UTF-8',
        'authority': 'chrome.google.com',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, '
                      'like Gecko) Ubuntu Chromium/69.0.3497.81 Chrome/69.0.3497.8'
                      '1 Safari/537.36',
    }

    last_update = '20180301'
    # taken from urllib.parse.unquote(url)
    mce = 'atf,pii,rtr,rlb,gtc,hcn,svp,wtd,nrp,hap,nma,nsp,c3d,ncr,ctm,ac,' + \
          'hot,mac,fcf,rma,irt,scm,qso,hrb,rae,shr,uid,dda,pot,evt'
    url = 'https://chrome.google.com/webstore/ajax/item?hl=en-US&gl=US&pv=' + \
          f'&pv={last_update}&mce={quote(mce)}&count=112&searchTerm={text}' + \
          '&sortBy=0&container=CHROME&_reqid=' + \
          f'{random.randint(200000, 800000)}&rt=j'
    data = 'login=&'
    res = requests.post(url, headers=headers, data=data)
    crx_json = deobfuscate_output(res.text)
    # convert back to human readable form
    extensions = [{
      'crx': val[0],
      'name': val[1],
      'desc': val[6]
    } for val in crx_json]
    return {
        'count': len(extensions),
        'extensions': extensions
    }


def main():
    """Main function"""
    terms_count = 0
    # get all terms to install / search for
    try:
        terms = sys.argv[1:]
        terms_count = len(terms)
    except IndexError:
        pass
    # if no terms, check for CEM_FILE
    if terms_count == 0:
        if os.path.exists(CEM_FILE):
            with open(CEM_FILE, 'r') as f:
                terms = f.readlines()
        else:
            # if no file, exit
            print("Usage: cem <search terms>")
            sys.exit(0)
    # make extensions directory
    if not os.path.exists(CRX_DIR):
        os.makedirs(CRX_DIR)
        if not os.path.exists(CRX_DIR):
            print(f'Cannot create {CRX_DIR}')
            sys.exit(0)
    # search for each term and download the first extension
    for term in terms:
        content = search(term)
        try:
            first = content['extensions'][0]
        except IndexError:
            print(f'Could not find {term}')
            continue
        file_path = get_crx_path(first['crx'], CRX_DIR)
        print(f'{first["name"]} downloaded to {file_path}')
        if not os.path.exists(file_path):
            # download(first['crx'], file_path)
            open_window(first['crx'])
        else:
            print('... already exists')


if __name__ == '__main__':
    main()
