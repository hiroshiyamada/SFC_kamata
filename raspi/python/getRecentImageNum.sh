#!/bin/bash

echo "Content-type: text/html"
echo ""

ls -1 images | sed -e 's/.jpg//' |tail -1
