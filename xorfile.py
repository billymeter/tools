#!/usr/bin/env python
'''
This is a tool that encrypts files with xor and a key. The contents of the file will be xored on a
byte by byte basis with the key, until the end of the length of the key. Once the end of the key
is reached, the xor operation will resume beginning at the start of the key until the entire file
has been encrypted.
'''

import argparse
import sys

#def xor_file (filename, key, create_backup=False):
    


def main():
    parser = argparse.ArgumentParser(prog=sys.argv[0],
                                     description='xor a file with a provided key.',
                                     epilog='')
    parser.add_argument('filename', metavar='file', 
                        help='Filename of the file to encrypt')
    parser.add_argument('key', metavar='key', 
                        help='Key to use for the xor operation')
    parser.add_argument('--backup', metavar='b', 
                        help='Create a backup of the file')

    args = parser.parse_args()

if __name__ == "__main__":
    main()
