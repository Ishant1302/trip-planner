import os
import hashlib
import pandas as pd
from collections import defaultdict

df = pd.read_csv('backend/datasets/places.csv')
front_dir = 'frontend/public/uploads'

dest_places = defaultdict(list)
for idx, row in df.iterrows():
    fname = os.path.basename(row['image'])
    fp = os.path.join(front_dir, fname)
    with open(fp, 'rb') as f:
        h = hashlib.md5(f.read()).hexdigest()
    dest_places[row['destination']].append((row['place_name'], fname, h))

found_duplicates = False
for dest, places in dest_places.items():
    hashes = {}
    for pname, fname, h in places:
        if h in hashes:
            print(f'Duplicate in {dest}: "{pname}" and "{hashes[h]}" share same image ({fname})!')
            found_duplicates = True
        else:
            hashes[h] = pname

if not found_duplicates:
    print('PERFECT: ALL ATTRACTIONS IN EVERY DESTINATION HAVE 100% UNIQUE IMAGES!')

