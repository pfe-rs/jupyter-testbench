#!/bin/sh

dir="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
users_dir="$HOME/users"
python_libs="$(python3 -m site --user-site)"
user_libs="$(echo "$python_libs" | sed "s:$HOME::")"

dataset_users="$dir/datasets"
dataset_bench="$dir/testbench/tests/datasets"

for user in $(find "$users_dir" -maxdepth 1 -mindepth 1 -type d); do
    if [ -L "$user/dataset" ]; then
        echo "delete $user/dataset"
        rm -f "$user/dataset"
    fi
    echo "link $dataset_users -> $user/dataset"
    ln -s "$dataset_users" "$user/dataset"

    if [ -e "$user$user_libs" ]; then
        echo "delete $user$user_libs"
        rm -rf "$user$user_libs"
    else
        parent="$(dirname "$user$user_libs")"
        echo "mkdir $parent"
        mkdir -p "$parent"
    fi
    echo "link $python_libs -> $user$user_libs"
    ln -s "$python_libs" "$user$user_libs"
done

if [ -L "$user/dataset" ]; then
    echo "delete $python_libs/testbench/tests/datasets"
    rm -f "$python_libs/testbench/tests/datasets"
fi
echo "link $dataset_bench -> $python_libs/testbench/tests/datasets"
ln -s "$dataset_bench" "$python_libs/testbench/tests/datasets"

