#!/bin/sh

echo $1

echo env is $GREETING

exec gunicorn --bind $PORT --workers 1 --threads $THREADS --timeout 0 app:app
