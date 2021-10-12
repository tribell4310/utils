#!/bin/bash

mkdir test
for filename in *; do
  if [ "${filename: -4}" == ".png" ]
  then
    mv $filename ./test/
  fi
done

