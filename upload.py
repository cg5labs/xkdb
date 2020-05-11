#!/usr/bin/env python3

"""
Dropbox upload script
"""

import argparse
import os
import pathlib
import re
import uuid
import logging
import dropbox

TARGET_FILENAME = str(uuid.uuid4())[:12]

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file", help="file path to upload")
args = parser.parse_args()

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO, \
                    datefmt='%Y-%m-%d %H:%M:%S', \
                    handlers=[ \
                        logging.FileHandler("upload.log"), \
                        logging.StreamHandler() \
                    ])

API_TOKEN = os.environ['API_TOKEN']

# the source file
local_filename = pathlib.Path(args.file)
logging.info("Source file to upload: %s", local_filename)

# target location in Dropbox
TARGET = "/"                             # the target folder
TARGETFILE = TARGET + TARGET_FILENAME    # the target path and file name

# Create a dropbox object using an API v2 key
d = dropbox.Dropbox(API_TOKEN)

# open the file and upload it
with local_filename.open("rb") as f:
    # upload gives you metadata about the file
    # we want to overwite any previous version of the file
    meta = d.files_upload(f.read(), TARGETFILE, mode=dropbox.files.WriteMode("overwrite"))

# create a shared link
link = d.sharing_create_shared_link(TARGETFILE)

# url which can be shared
url = link.url

# link which directly downloads by replacing ?dl=0 with ?dl=1
dl_url = re.sub(r"\?dl\=0", "?dl=1", url)
logging.info("Dropbox URL: %s", dl_url)
