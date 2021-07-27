#!/usr/bin/env bash

# start custom
APP_PATH=/Users/User/coding_local/xkdb
CFG_PATH="${HOME}"
# end custom

UPLOAD=$1
RC=0

cd ${APP_PATH} || exit 1

# sanity checks

# check input parameter
if [[ -z ${UPLOAD} ]]; then
  echo "Usage: $(basename "$0") <filename>"
  RC=1
fi

# check if local file exists
if [[ ! -f ${UPLOAD} ]]; then
  echo "Upload file not found: ${UPLOAD}"
  RC=2
fi

# check if Python venv exists
if [[ -d venv/bin ]]; then
  # shellcheck source=/dev/null
  source venv/bin/activate
  else
    echo "VirtualEnv missing. Instaling Virtualenv ... "
    #virtualenv -p /usr/local/bin/python3 venv
    python3 -m venv venv
    # shellcheck source=/dev/null
    source venv/bin/activate
    pip3 install -r requirements.txt
    RC=3
fi

# check if config file exists
if [[ -r "${CFG_PATH}/.dropbox" ]]; then
  # shellcheck source=/dev/null
  source "${CFG_PATH}"/.dropbox
else
  echo "Config file not found: ${CFG_PATH}/.dropbox"
  RC=3
fi

# main
if [[ $RC == 0 ]]; then
  ./upload.py -f "${UPLOAD}"
  RC=$?
fi

exit $RC
