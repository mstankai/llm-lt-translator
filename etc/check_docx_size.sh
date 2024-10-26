#!/bin/bash
if [ "$(wc -c < "$1")" -gt 5242880 ]; then
    echo "Error: Large DOCX file"
    exit 1
fi
