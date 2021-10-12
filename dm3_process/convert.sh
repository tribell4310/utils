#!/bin/bash

for filename in *; do
  echo $filename
  if [ "${filename: -4}" == ".dm3" ]
  then
    prefix=$(echo $filename | cut -d'.' -f 1)
    suffix="_convert.mrc"
    dm2mrc $filename "$prefix$suffix"
  fi
done

