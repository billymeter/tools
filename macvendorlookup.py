#!/usr/bin/env python
'''Looks up a company ID for a given MAC address.'''

import requests
import argparse
import sys
import cPickle as pickle

# Link to the OUI file that contains the company IDs
oui_file = 'http://standards-oui.ieee.org/oui.txt'

# Global for the database dictionary that must be loaded
database = {}

def download_oui_file():
    filename = oui_file.split('/')[-1]
    print 'Now attempting to download data to create the database. This might take a few minutes...'
    try:
        req = requests.get(oui_file, stream=True)
    except:
        print 'Cannot access %s. Are you connected to the Internet?' % oui_file
        sys.exit(1)

    try:
        with open(filename, 'wb') as f:
            for chunk in req.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
                    f.flush()
    except:
        print 'Can\'t write to file %s' % filename
        sys.exit(1)

def create_database():
    download_oui_file()
    global database
    try:
        with open('oui.txt','r') as f:
            contents = f.readlines()
    except:
        print 'Couldn\'t open oui.txt!'
        sys.exit(1)

    entries = [y.lstrip().split('     (base 16)\t\t') for y in [x.strip('\n') for x in contents if "(base 16)" in x]]
    database = {d[0]: d[1] for d in entries}

    try:
        with open('ouis.db', 'wb') as f:
            pickle.dump(database, f, pickle.HIGHEST_PROTOCOL)
    except:
        print 'Cannot write database!'
        sys.exit(1)

def load_database():
    global database
    try:
        with open('ouis.db','rb') as f:
            database = pickle.load(f)
    except:
        print 'Cannot load database. Attempting to create the database...'
        create_database()

def mac_format(mac):
   proc = mac.translate(None, ' :.-')
   return proc[:6].upper()

def mac_lookup(mac):
    try:
        print '%s   %s' % (mac, database[mac_format(mac)])
    except:
        print 'OUI for MAC does not exist, or \'%s\' was not a MAC address' % mac

def mac_file_lookup(filename):
    try:
        with open(filename, 'r') as f:
            macs = f.readlines()
    except:
        print '%s is an invalid filename or you do not have permissions to read it' % filename
        sys.exit(1)

    for m in macs:
        mac_lookup(m.strip('\n'))

def main():
    parser = argparse.ArgumentParser(prog=sys.argv[0],
                                     description='Look up which company manufactured a network\
                                     card by the MAC address.')
    parser.add_argument('mac', metavar='mac', nargs='?',
                        help='MAC address to look up')
    parser.add_argument('-f', '--loadfile', metavar='filename',
                        help='Load list of MACs, one per line')
    parser.add_argument('-d', '--database', action='store_true',
                        help='Recreate the OUI lookup database')
    args = parser.parse_args()

    if args.database:
        create_database()
        print 'Database created!'
        if not args.mac and not args.loadfile:
            return 0

    load_database()

    if args.loadfile:
        mac_file_lookup(args.loadfile)
        return 0

    if args.mac:
        mac_lookup(args.mac)
        return 0

    parser.print_help()
    return 0

if __name__ == "__main__":
    main()
