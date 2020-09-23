#!/usr/bin/env bash

# D FOUCHE
# UCT CS HONS
# fchdyl001@myuct.ac.za

set -x

#
# Run performance tests from disk
#

/data/cadaflop/Build/CARTA/carta-backend/build/carta_backend -base /data/cadaflop/Data >/dev/null &
sleep 5

# Test against CARTA
./main.py -pc

# Test against Dask local
./main.py -p

# Test against Dask distributed
./main.py -pd

pkill carta_bac
pkill python3

#
# Run performance tests from memory
#

/data/cadaflop/Build/CARTA/carta-backend/build/carta_backend -base /ramdisk >/dev/null &
sleep 5

# Test against CARTA
./main.py -pcm

# Test against Dask local
./main.py -pm

# Test against Dask distributed
./main.py -pdm

pkill carta_bac
pkill python3

#
# Run unit tests
#

/data/cadaflop/Build/CARTA/carta-backend/build/carta_backend -base /data/cadaflop/Data >/dev/null &
sleep 5

./main.py -t

pkill carta_bac

set -x
