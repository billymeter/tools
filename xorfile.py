#!/usr/bin/env python
'''
This is a tool that encrypts files with xor and a key. The contents of the file will be xored on a
byte by byte basis with the key, until the end of the length of the key. Once the end of the key
is reached, the xor operation will resume beginning at the start of the key until the entire file
has been encrypted.
'''

import argparse
import sys

def xor_string(string, key):
    '''Simple xor of two strings'''
    output = ''
    i = 0
    l = len(key)
    for c in list(string):
        output += chr(ord(c) ^ ord(key[i % l]))
        i += 1
    return output

def xor_file (filename, key, backup_filename=''):
    '''Wrapper to xor_string that works with files'''
    try:
        with open(filename, 'r') as f:
            contents = f.read()
    except:
        print "%s does not exist or you do not have permissions to read it." % filename
        sys.exit(1)

    enc = xor_string(contents, key)

    if backup_filename:
        try:
            with open(backup_filename, 'w') as f:
                f.write(contents)
        except:
            print "You do not have permissions to write %s to this directory" % backup_filename
            sys.exit(1)

    try:
        with open(filename, 'w') as f:
            f.write(enc)
    except:
        print "You do not have permissions to write %s to this directory" % filename
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(prog=sys.argv[0],
                                     description='xor a file with a provided key.',
                                     epilog='')
    parser.add_argument('filename', metavar='file', 
                        help='Filename of the file to encrypt')
    parser.add_argument('key', metavar='key', 
                        help='Key to use for the xor operation')
    parser.add_argument('--backup', metavar='filename', 
                        help='Create a backup of the file')

    args = parser.parse_args()

    xor_file(args.filename, args.key, args.backup)

if __name__ == "__main__":
    main()
