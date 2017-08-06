#!/usr/bin/python3

from Crypto.Cipher import DES
from json import dump
from os.path import expanduser
from xml.etree import ElementTree
from xmljson import gdata

import errno
import os
import re
import sys
import zlib

if len(sys.argv) < 2:
    print('usage: ' + sys.argv[0] + ' <path to albion gamedir>')
    sys.exit()

key = bytes([0x30, 0xef, 0x72, 0x47, 0x42, 0xf2, 0x4, 0x32])
iv = bytes([0xe, 0xa6, 0xdc, 0x89, 0xdb, 0xed, 0xdc, 0x4f])

items = ['accessrights', 'achievements', 'agentreferences', 'agents',
        'audio', 'buildings', 'characters', 'emotes',
        'expeditionagents', 'expeditioncategories', 'expeditions',
        'factions', 'gamedata', 'itemroles', 'items',
        'localization', 'loot', 'missions', 'mobs', 'resourcedistpresets',
        'resources', 'sockets', 'spells', 'territorytypes',
        'treasures', 'worldbosses', 'worldsettings']

input_path = expanduser(sys.argv[1] + '/Albion-Online_Data/StreamingAssets/GameData/')
output_path = './output/'

try:
    os.makedirs(output_path)
except OSError as e:
    if e.errno != errno.EEXIST:
        raise

def export_item(item, outpath):
    cipher = DES.new(key, DES.MODE_CBC, iv)

    with open(item, 'rb') as input:
        decrypted = cipher.decrypt(input.read())
        xml = zlib.decompress(decrypted, 16+zlib.MAX_WBITS).decode('utf-8')
        # xml_schemaless = re.sub(' xmlns:xsi="[^>]+"', '', xml, count=1)

        json = gdata.data(ElementTree.fromstring(xml))
        with open(outpath + '.json', 'w') as out:
            dump(json, out, indent=4)

        with open(outpath + '.xml', 'w') as out:
            out.write(xml)

for item in items:
    print('Processing ' + item + ' ...')
    export_item(input_path + item + '.bin', output_path + item)
