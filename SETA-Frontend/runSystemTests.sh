#!/bin/bash

# Get script's location regardless of where it was executed from
CUR_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
PARENT_DIR=$(dirname ${CUR_DIR})

# Install if not existing and once installed don't update.
if [ $(which python3 | wc -l) -ne 1 ]; then
  echo "Installing Requirements: python3, python3-pip, python3-venv"
  sudo apt-get install -y python3 python3-pip python3-venv
  fi
if [ $(which Xvfb | wc -l) -ne 1 ]; then
  echo "Installing Requirement: Xvfb"
  sudo apt-get install -y python3 python3-pip python3-venv
        echo "Setting up virtual framebuffer "
      Xvfb -noreset :0 >& /dev/null &
      export DISPLAY=:0.0
  fi

# Create virtual env
python3 -m venv $CUR_DIR/venv
source $CUR_DIR/venv/bin/activate
pip install -r $PARENT_DIR/requirements.txt
cd $CUR_DIR

# Install chrome and firefox if not installed.
if [ $(which geckodriver | wc -l) -ne 1 ]; then
  webdrivermanager firefox
  fi

echo ----------------------$(which geckodriver)
python  ExecuteTestCases.py

# if webdriver still affected by bug 5672, use  sudo apt install firefox-geckodriver