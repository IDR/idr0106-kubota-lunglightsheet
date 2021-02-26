#!/usr/bin/env python
# Generate companion files

import re
import os
from ome_model import experimental as ome

BASE_DIRECTORY = "/uod/idr/filesets/idr0106-kubota-lunglightsheet/20210226"

FORMAT = ".*\[(\d{5})\]_L\[(\d)\]\.ome\.tiff"
#                 Z        ChI

SIZE_X = 4992
SIZE_Y = 4255
SIZE_Z = 0
SIZE_T = 1
SIZE_C = 3

IMAGE_FILES_SRC = "idr0106_files.txt"
OUTPUT_DIR = "../experimentA/companions"
IMAGE_NAME = "Mosaic_Image"


image_files = open(IMAGE_FILES_SRC, 'r').readlines()

for file in image_files:
    if match := re.search(FORMAT, file, re.IGNORECASE):
        z_index = int(match.group(1))
        SIZE_Z = max(z_index, SIZE_Z)


companion = ome.Image(IMAGE_NAME, SIZE_X, SIZE_Y, SIZE_Z, SIZE_C,
    sizeT=SIZE_T, order='XYZCT', type='uint16')
companion.add_channel(name="alpha-SMA-FITC", samplesPerPixel=1)
companion.add_channel(name="VEGFR3-Alexa546", samplesPerPixel=1)
companion.add_channel(name="A549-mCherry", samplesPerPixel=1)

for file in image_files:
    file = file.strip()
    ln_src = BASE_DIRECTORY+"/"+file
    ln_tgt = OUTPUT_DIR+"/"+file
    if not os.path.islink(ln_tgt):
        os.symlink(ln_src, ln_tgt)
    if match := re.search(FORMAT, file, re.IGNORECASE):
        z_index = int(match.group(1)) - 1
        channel_index = int(match.group(2)) - 1
        companion.add_tiff(file, c=channel_index, t=1, z=z_index, planeCount=1)

companion_file = OUTPUT_DIR+"/"+IMAGE_NAME+".companion.ome"
if os.path.exists(companion_file):
    os.remove(companion_file)

with open(companion_file, 'wb') as o:
    ome.create_companion(images=[companion], out=o)
