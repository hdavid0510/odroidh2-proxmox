#!/bin/bash

for d in {0..4}; do
        if [ "$(i2cdetect -y -r $d | grep 3c)" != "" ]; then
                echo -n $d
                exit $d
        fi
done
