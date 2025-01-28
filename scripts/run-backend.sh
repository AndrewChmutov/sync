#!/bin/sh

cd ../backend
source .venv/bin/activate
python3 -m sync.main
