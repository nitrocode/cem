#!/usr/bin/env python3
import sys
import json
import os
import requests
import random
from urllib.parse import quote
from urllib.request import urlretrieve


CRX_DIR = 'extensions'
CEM_FILE = 'Cemfile'


def get_crx_path(uid, directory):
    """Return the local crx path for an extension

    :param uid: crx unique identifier
    :return: local crx path
    """
    return os.path.join(directory, '{}.crx'.format(uid))


def download(uid, file_path):
    """Download the crx using the crx uid

    :param uid: crx unique identifier
    :return: true if the file is downloaded
    """
    url = 'https://clients2.google.com/service/update2/crx'
    url += '?response=redirect&prodversion=49.0&x=id%3D'
    url += '{}%26installsource%3Dondemand%26uc'
    crx_url = url.format(uid)
    urlretrieve(crx_url, file_path)
    return os.path.exists(file_path)


def search(text):
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

    lastUpdate = '20180301'
    # taken from urllib.parse.unquote(url)
    mce = 'atf,pii,rtr,rlb,gtc,hcn,svp,wtd,nrp,hap,nma,nsp,c3d,ncr,ctm,ac,' + \
          'hot,mac,fcf,rma,irt,scm,qso,hrb,rae,shr,uid,dda,pot,evt'
    url = 'https://chrome.google.com/webstore/ajax/item?hl=en-US&gl=US&pv={}' + \
          '&mce={}&count=112&searchTerm={}&sort' + \
          'By=0&container=CHROME&_reqid={}&rt=j'
    url = url.format(lastUpdate, quote(mce), text, random.randint(200000, 800000))
    data = 'login=&'
    res = requests.post(url, headers=headers, data=data)
    crx_json = json.loads(res.text[4:].replace('\n', ''))[0][1][1]
    extensions = [{'crx': val[0], 'name': val[1], 'desc': val[6]}
                  for val in crx_json]
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
    except:
        pass
    # if no terms, check for Crxfile
    if terms_count == 0:
        if os.path.exists(CEM_FILE):
            with open(CEM_FILE, 'r') as f:
                terms = f.readlines()
                terms_count = len(terms)
        else:
            # if no file, exit
            print("Usage: cem <search terms>")
            sys.exit(0)
    # make extensions directory
    if not os.path.exists(CRX_DIR):
        os.makedirs(CRX_DIR)
        if not os.path.exists(CRX_DIR):
            print('Cannot create {}'.format(CRX_DIR))
            sys.exit(0)
    # search for each term and download the first extension
    for term in terms:
        content = search(term)
        first = content['extensions'][0]
        file_path = get_crx_path(first['crx'], CRX_DIR)
        print('{} downloaded to {}'.format(first['name'], file_path))
        if not os.path.exists(file_path):
            download(first['crx'], file_path)
        else:
            print('... already exists')


if __name__ == '__main__':
    main()
