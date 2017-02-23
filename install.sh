#!/bin/bash
pip install -r requirements.txt
case "$(uname -s)" in
  Darwin)
    echo 'Install numpy and scipy for Mac'
    ;;
  Linux)
    apt-get install python-numpy python-scipy
    ;;
esac
