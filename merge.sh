#!/usr/local/bin/bash

for i in $@; do
  echo buggy_$i
  files=$(colordiff -qr buggy_$i/src fix_$i/src | cut -f 4 -d " " | cut -d "/" -f2-100)
  for f in $files; do
    #echo $f
    echo cp buggy_$i/$f merged2/$f
    cp buggy_$i/$f merged2/$f
  done
  echo Done
  echo =======================
done
