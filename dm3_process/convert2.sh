#!/bin/bash

for filename in *; do
  echo $filename
  if [ "${filename: -4}" == ".mrc" ]
  then
    prefix=$(echo $filename | cut -d'.' -f 1)
    suffix="_asPic.png"
    proc2d $filename "$prefix$suffix"
  fi
done

