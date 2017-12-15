#!/bin/bash

if [ -z ${MAHMOUD_KEYSTORE+x} ]; then
    echo 'ERROR: environment variable MAHMOUD_KEYSTORE is not set'
    exit 1
fi

if [  -z ${1+x} ]; then
    echo 'ERROR: no apk provided as input'
    exit 2
fi
    

jarsigner -verbose -sigalg SHA1withRSA -digestalg SHA1 -keystore $MAHMOUD_KEYSTORE -storepass mahmoud -keypass mahmoud $1 mahmoud









