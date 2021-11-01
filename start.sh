#!/bin/bash
PY_VIRTUALENV=$(ls ~/.local/share/virtualenvs | grep AntOS-API)

sudo FLASK_ENV=development /home/clement/.local/share/virtualenvs/$PY_VIRTUALENV/bin/python -m flask run -h 0.0.0.0 -p 80
