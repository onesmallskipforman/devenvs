#!/bin/sh

# flashthing was recommended via
# https://github.com/usenocturne/nocturne/issues/34. meta.json is required to
# be in the same directory as all of the files to be flashed. meta.json was
# found at https://github.com/JoeyEamigh/flashthing/blob/77d93d6d352a82ec85d94447ec737e6387f21252/lib/resources/stock-meta.json
# with a typo fixed (env.dump -> env.txt)
# typo was found by looking at example meta.json files on discord
# https://discord.gg/mnURjt3M6m
# NOTE: as per https://github.com/usenocturne/nocturne?tab=readme-ov-file#setting-up-network,
# make sure to test car thing connect to an outlet, as running connected to a
# computer can cause issues with conncting via bluetooth

# as a fallback you can use terbium.app:
# https://github.com/usenocturne/nocturne?tab=readme-ov-file#flashing

unzip -d nocturne nocturne_image_v3.0.0.zip
cp meta.json nocture
./flashthing-cli-linux-x86_64 --setup
./flashthing-cli-linux-x86_64 ./nocturne
