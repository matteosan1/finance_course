#! /bin/bash

for n in {0..1000}
do
    mv plt_$n.png plt_$(printf "%04d" $n).png
done
