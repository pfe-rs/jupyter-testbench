#!/bin/sh

dir="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
users_dir="$HOME/users"
py_libs="$(python3 -m site --user-site)"

dataset_users="$dir/datasets"
dataset_bench="$dir/testbench/tests/datasets"

for user in $(find "$users_dir" -maxdepth 1 -mindepth 1 -type d); do
    if [ -L "$user/dataset" ]; then
        echo "delete $user/dataset"
        rm -f "$user/dataset"
    fi
    echo "$dataset_users -> $user/dataset"
    ln -s "$dataset_users" "$user/dataset"
done

if [ -L "$user/dataset" ]; then
    echo "delete $py_libs/testbench/tests/datasets"
    rm -f "$py_libs/testbench/tests/datasets"
fi
echo "$dataset_bench -> $py_libs/testbench/tests/datasets"
ln -s "$dataset_bench" "$py_libs/testbench/tests/datasets"
