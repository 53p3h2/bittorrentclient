import sys
import os
from bcoding import bencode,bdecode
import hashlib
import time

#getting and parsing the torrent file
torrent_file = sys.argv[1]
with open(torrent_file, 'rb') as file:
    contents = bdecode(file)
piece_length = contents['info']['piece length']
pieces = contents['info']['pieces']
raw_info_hash = bencode(contents['info'])
info_hash = hashlib.sha1(raw_info_hash).digest()
peer_id = hashlib.sha1(str(time.time()).encode('utf-8')).digest()
announce_list = contents['announce-list'] if 'announce-list' in contents else contents['announce']
root = contents['info']['name']
file_names = []
total_length : int=0

#crating directories for files mentioned in info section
if 'files' in contents['info']:
    if not os.path.exists(root):
        os.mkdir(root,0o0766)
    for file in contents['info']['files']:
        path_file = os.path.join(root, *file['path'])
        if not os.path.exists(os.path.dirname(path_file)):
            os.makedirs(os.path.dirname(path_file))
        file_names.append({"path" : path_file, "length" : file["length"]})
        total_length += file["length"]
else:
    file_names.append({"path" : root, "length" : contents['info']['length']})
    total_length = contents['info']['length']

