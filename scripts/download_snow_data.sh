#!/bin/bash

# Downloads snow depth and density data from NSIDC 0758 Langrangian Snow Distributions

OUTDIR="$HOME/Data/Sunlight_under_seaice/SnowModelData"

# Check a .netrc file is in $HOME
if [ ! -f "$HOME/.netrc" ]; then
    echo ".netrc not found in $HOME"
    exit 1
fi

if [ ! -d $OUTDIR ]; then
    echo "$OUTDIR does not exist, creating it"
    mkdir -p $OUTDIR
fi

URL="https://daacdata.apps.nsidc.org/pub/DATASETS/nsidc0758_lagrangian_snow_distributions_v01/"

OPTS='--load-cookies ~/.urs_cookies --save-cookies ~/.urs_cookies --keep-session-cookies --no-check-certificate --auth-no-challenge=on -r --reject "index.html*" -np -e robots=off'

wget $OPTS -nd -P $OUTDIR $URL
