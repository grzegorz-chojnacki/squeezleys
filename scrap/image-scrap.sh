#!/bin/bash

set -xe

URLS='./image-urls'
IMAGEDIR='../data/images'

cat "$URLS" | while read url
do
  filename=$(echo $url | cut -c 29- | sed -e 's/\//-/g')
  wget "$url" -O "$IMAGEDIR/$filename"
done
