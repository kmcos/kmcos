#!/bin/bash

# This is a simple script to test all of the throttling cases.

throttling_case_min=1
throttling_case_max=7
throttling_cases=$(seq $throttling_case_min $throttling_case_max)

for tc in $throttling_cases; do
  sed -i "8 s/[[:digit:]]\{1,\}/$tc/" test_throttle_function.py
  sed -n '8p' test_throttle_function.py
  ./test_throttle_function.py
done
