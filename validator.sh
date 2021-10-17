#!/bin/sh

remove_user_examples() {
    ! grep -qF 'def fibonacci(n: int) -> int:' ./user_demo.py && \
    ! grep -qF 'def factorial(n: int) -> int:' ./user_demo.py && \
    ! grep -qF 'def is_even(n: int) -> bool:' ./user_demo.py && \
    ! grep -qF 'def binarization(image: np.ndarray) -> np.ndarray:' ./user_demo.py
}

remove_test_examples() {
    ! test -f ./testbench/tests/fibonacci.py && \
    ! test -f ./testbench/tests/factorial.py && \
    ! test -f ./testbench/tests/is_even.py && \
    ! test -f ./testbench/tests/binarization.py && \
    ! test -d ./testbench/tests/datasets/binarization
}

tests="$(
    find ./testbench/tests -maxdepth 1 -type f \
        -name '*.py' -not -name '__init__.py' -printf '%P\n' |\
    sed 's/\.py$//'
)"

test_import() {
    for t in $tests; do
        grep -qF "from .$t import test_$t" ./testbench/tests/__init__.py || return 1
    done
}

test_ref_impl() {
    for t in $tests; do
        grep -q "def $t(.*) -> .*:" ./user_demo.py || return 1
    done
}

test_run() {
    for t in $tests; do
        grep -qF "Testbench($t)" ./user_demo.py || return 1
    done
}

user_demo() {
    output="$(python ./user_demo.py)"
    for t in $tests; do
        echo "$output" | grep -qF "Funkcija '$t' uspešno prolazi sve testove." || return 1
    done
}

if [ $# = 1 ]; then
    $1;
else
    remove_user_examples && \
    remove_test_examples && \
    test_import && \
    test_ref_impl && \
    test_run && \
    user_demo
fi
