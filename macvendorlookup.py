#!/usr/bin/env python
'''Looks up a company ID for a given MAC address.'''

import requests
import argparse
import sys

# Link to the OUI file that contains the company IDs
oui_file = 'http://standards-oui.ieee.org/oui.txt'

def download_oui_file():
    filename = oui_file.split('/')[-1]
    req = requests.get(oui_file, stream=True)

    try:
        with open(filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
                    f.flush()
    except:
        print 'Can\'t write to file %s' % filename
        sys.exit(1)

def create_database(oui):


def main():
    parser = argparse.ArgumentParser(prog=sys.argv[0],
                                     description='Look up which company manufactured a network\
                                     card by the MAC address.')
    parser.add_argument('mac', metavar='mac', nargs='?',
                        help='MAC address to look up')
    parser.add_argument('-f', '--file', metavar='file',
                        help='Load list of MACs, one per line')
    parser.add_argument('-d', '--database', metavar='',
                        help='Recreate the OUI lookup database')
    args = parser.parse_args()

if __name__ == "__main__":
    main()
