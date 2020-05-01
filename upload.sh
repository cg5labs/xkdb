#!/usr/bin/env bash

UPLOAD=$1
RC=0
APP_PATH=/Users/User/coding_local/python/xkdb

cd ${APP_PATH}

if [[ -z ${UPLOAD} ]]; then
  echo "Usage: $(basename $0) <filename>"
  RC=1
fi

if [[ ! -f ${UPLOAD} ]]; then
  echo "Upload file not found! ${UPLOAD}"
  RC=2
fi

if [[ $RC == 0 ]]; then
  if [[ -d venv/bin ]]; then
    source venv/bin/activate
    source $HOME/.dropbox
    ./upload.py -f "${UPLOAD}"
    RC=$?
  else
    echo "VirtualEnv missing. Instaling Virtualenv ... "
    virtualenv -p /usr/local/bin/python3 venv
    source venv/bin/activate
    pip3 install -r requirements.txt
    RC=3
  fi
fi

exit $RC
