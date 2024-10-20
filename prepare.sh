#!/bin/sh

[ -n "${PY}" ] || PY=python3

"${PY}" -m venv venv \
	&& . venv/bin/activate \
	&& python -m pip install --upgrade pip \
	&& python -m pip install -r requirements.txt
