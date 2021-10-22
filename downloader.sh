#!/bin/sh

dir="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"

lists="$(
    find "$dir/datasets" "$dir/testbench/tests/datasets" \
        -type f -name 'download.txt'
)"

for list in $lists; do
    cd "$(dirname "$list")" || exit 1
    cat <"$list" | while IFS= read -r line; do
        curl -L -o ./data.zip "$line" &&
            unzip -u ./data.zip &&
            rm ./data.zip
    done
done
