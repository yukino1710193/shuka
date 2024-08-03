#!/bin/bash

if [ $1 == "success" ]; then
    exit 0
elif [ $1 == "failed" ]; then
    exit 1
fi
