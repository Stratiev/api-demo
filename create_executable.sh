#/bin/bash

set -e

pyinstaller --onefile external_executable.py
cp dist/external_executable .
rm -rf dist build external_executable.spec
