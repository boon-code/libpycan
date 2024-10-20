#!/bin/sh

. ./venv/bin/activate && \
   python compile.py && \
   gcc -o app main.c -L. -lpycan -Wl,-rpath=. && \
   ./app
