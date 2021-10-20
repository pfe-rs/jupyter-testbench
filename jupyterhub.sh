#!/bin/sh

dir="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
users_dir="/home"
cd /tmp # If we're in the testbench directory this 

dataset_users="$dir/datasets"
dataset_bench="$dir/testbench/tests/datasets"

for user in $(find "$users_dir" -maxdepth 1 -mindepth 1 -type d); do
    if [ -L "$user/dataset" ]; then
        echo "delete $user/dataset"
        rm -f "$user/dataset"
    fi
    echo "link $user/dataset -> $dataset_users"
    ln -s "$dataset_users" "$user/dataset"
done
