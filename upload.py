#!/usr/bin/env python3

import argparse
import dropbox
import os
import pathlib
import re
import sys
import uuid

target_filename = str(uuid.uuid4())[:8] + ".kdbx"

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file", help="file path to upload")
args = parser.parse_args()

api_token = os.environ['API_TOKEN']

# the source file
local_filename = pathlib.Path(args.file)

# target location in Dropbox
target = "/"              # the target folder
targetfile = target + target_filename  # the target path and file name

# Create a dropbox object using an API v2 key
d = dropbox.Dropbox(api_token)

# open the file and upload it
with local_filename.open("rb") as f:
   # upload gives you metadata about the file
   # we want to overwite any previous version of the file
   meta = d.files_upload(f.read(), targetfile, mode=dropbox.files.WriteMode("overwrite"))

# create a shared link
link = d.sharing_create_shared_link(targetfile)

# url which can be shared
url = link.url

# link which directly downloads by replacing ?dl=0 with ?dl=1
dl_url = re.sub(r"\?dl\=0", "?dl=1", url)
print (dl_url)
