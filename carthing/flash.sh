#!/bin/sh

unzip -d nocturne nocturne_image_v3.0.0.zip
cp meta.json nocture
./flashthing-cli-linux-x86_64 --setup
./flashthing-cli-linux-x86_64 ./nocturne
