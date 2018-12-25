#!/bin/bash

echo "Content-type: text/html"
echo ""
cat - > test.fifo
#cat - | xargs -n4 beep
echo beep
