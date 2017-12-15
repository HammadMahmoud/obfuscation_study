#!/bin/bash

/usr/local/bin/aapt dump badging $1 | grep package:\ name | cut -d "'" -f2
