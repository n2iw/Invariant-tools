#!/usr/local/bin/bash

for i in {1..27}; do
  echo buggy_$i
  files=$(colordiff -qr buggy_$i/src fix_$i/src | cut -f 4 -d " " | cut -d "/" -f2-100)
  good="Good to go"
  for f in $files; do
    #echo $f
    colordiff -qr merged2/$f fix_$i/$f 
    if [ $? -ne 0 ]; then
      good="Different"
    fi
  done
  echo buggy_$i is $good
  echo =======================
done
