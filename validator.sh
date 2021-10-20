#!/bin/sh

git_branch() {
    if [ "$(git rev-parse --abbrev-ref HEAD)" = 'master' ]; then
        printf '\e[1;33mWarning:\e[0m Working on master branch!\n' >&2
    fi
}

remove_user_examples() {
    error_msg='User demo examples are not removed'
    ! grep -qF 'def fibonacci(n: int) -> int:' ./user_demo.py &&
        ! grep -qF 'def factorial(n: int) -> int:' ./user_demo.py &&
        ! grep -qF 'def is_even(n: int) -> bool:' ./user_demo.py &&
        ! grep -qF 'def binarization(image: np.ndarray) -> np.ndarray:' ./user_demo.py
}

remove_test_examples() {
    error_msg='Testbench examples are not removed'
    ! test -f ./testbench/tests/fibonacci.py &&
        ! test -f ./testbench/tests/factorial.py &&
        ! test -f ./testbench/tests/is_even.py &&
        ! test -f ./testbench/tests/binarization.py &&
        ! test -d ./testbench/tests/datasets/binarization
}

remove_notebook_example() {
    error_msg='User demo notebook is not removed'
    error_subj=''
    ! test -f './notebooks/User demo.ipynb'
}

tests="$(
    find ./testbench/tests -maxdepth 1 -type f \
        -name '*.py' -not -name '__init__.py' -printf '%P\n' |
        sed 's/\.py$//'
)"

test_import() {
    error_msg='Testbench test is not imported for '
    for t in $tests; do
        error_subj="$t"
        grep -qF "from .$t import test_$t" ./testbench/tests/__init__.py || return 1
    done
}

test_ref_impl() {
    error_msg='Referent implementation definition missing for '
    for t in $tests; do
        error_subj="$t"
        grep -q "def $t(.*) -> .*:" ./user_demo.py || return 1
    done
}

test_run() {
    error_msg='Testbench not called for referent implementation of '
    for t in $tests; do
        error_subj="$t"
        grep -qF "Testbench($t)" ./user_demo.py || return 1
    done
}

modules_user="$(
    awk '/^import/ { print $2 }; /^from .* import/ { if($2!="testbench") print $2; }' ./user_demo.py
)"

module_import_user() {
    error_msg='Potentially missing dependency in setup.py for user imported module '
    for m in $modules_user; do
        error_subj="$m"
        grep -q "install_requires=.*'$m'" ./setup.py || return 2
    done
}

modules_test="$(
    find ./testbench/tests -maxdepth 1 -type f -name '*.py' -not -name '__init__.py' -exec \
        awk '/^import/ { print $2 }; /^from .* import/ { if($2!="testbench") print $2; }' {} \;
)"

module_import_test() {
    error_msg='Potentially missing dependency in setup.py for Testbench imported module '
    for m in $modules_test; do
        error_subj="$m"
        grep -q "install_requires=.*'$m'" ./setup.py || return 2
    done
}

user_demo() {
    error_msg='Failed to pass the test for user demo for referent implementation of '
    output="$(python ./user_demo.py)"
    for t in $tests; do
        error_subj="$t"
        echo "$output" | grep -qF "Funkcija '$t' uspešno prolazi sve testove." || return 1
    done
}

git_branch

validate() {
    error_msg=''
    error_subj=''
    $1
    case $? in
    1)
        printf '\e[1;31mError:\e[0m %s\e[1m%s\e[0m!\n' "$error_msg" "$error_subj" >&2
        return 1
        ;;
    2)
        printf '\e[1;33mWarning:\e[0m %s\e[1m%s\e[0m!\n' "$error_msg" "$error_subj" >&2
        return 0
        ;;
    esac
}

if [ $# = 1 ]; then
    validate $1
else
    errors=0
    for v in 'remove_user_examples' 'remove_test_examples' 'remove_notebook_example' \
        'test_import' 'test_ref_impl' 'test_run' \
        'module_import_user' 'module_import_test' 'user_demo'; do
        if ! validate "$v"; then
            errors="$((errors + 1))"
        fi
    done
    if [ "$errors" = 0 ]; then
        printf '\e[1;32mSuccess:\e[0m Validator found no critical errors.\n' >&2
    fi
fi
