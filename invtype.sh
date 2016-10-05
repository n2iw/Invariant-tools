#!/bin/bash

if [ $# -lt 3 ]; then
  echo Usage $0 ignore.sed_script invariants.sed_script input_files
  exit 1
fi

for f in "${@:3}"; do
  echo =================
  echo "input file: $f"
  filename=${f##*/}
  filename=$(echo $filename | cut -d '.' -f1)
  filename=${filename}.inv
  echo "output file: $filename"
  if [ -f $filename ]; then
    mv $filename ${filename}.bak
  fi
  while read i; do
    pattern=$(echo $i | cut -d '/' -f2)
    grep -q "$pattern" $f
    if [ $? -eq 0 ]; then
      echo Found $pattern
      echo "$pattern" >> $filename
    fi
  done < $2

  sed -f $1 < $f | sed -f $2 $f >> $f.inv
done
