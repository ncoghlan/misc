#! /bin/sh
#
# Find git commits that include a given git tree ref
# Code from: https://stackoverflow.com/a/41090798/ 

searchfor=$1 # git tree ref hash of interest
startpoints="master"  # branch names or HEAD or whatever
# you can use rev-list limiters too, e.g., origin/master..master

git rev-list $startpoints |
    while read commithash; do
        if git ls-tree -d -r --full-tree $commithash | grep $searchfor; then
            echo " -- found at $commithash"
        fi
    done
