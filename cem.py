#!/usr/bin/env python
import urllib
import sys
import json
import os
import requests


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
    urllib.urlretrieve(crx_url, file_path)
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
    }

    url = 'https://chrome.google.com/webstore/ajax/item'
    url += '?hl=en&gl=US&pv=20170811&mce=atf%2Cpii%2Crtr%2Crlb%2Cgtc%2Chcn'
    url += '%2Csvp%2Cwtd%2Cnrp%2Chap%2Cnma%2Cc3d%2Cncr%2Cctm%2Cac%2Chot%2Cmac'
    url += '%2Cfcf%2Crma%2Cirt%2Cscm%2Cqso%2Chrb%2Crer%2Crae%2Cshr%2Cesl%2Cdda'
    url += '%2Cpot%2Cevt&count=112&searchTerm={}'
    url += '&sortBy=0&container=CHROME&_reqid=1962197&rt=j'
    url = url.format(text)
    data = 'login=&'
    res = requests.post(url, headers=headers, data=data)
    crx_json = json.loads(res.content[4:].replace('\n', ''))[0][1][1]
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
