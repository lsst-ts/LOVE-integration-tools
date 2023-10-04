#!/bin/bash
make html
# Create index.html
echo "<meta http-equiv='refresh' content='0; url=./html/index.html' />" > ../docs/index.html
