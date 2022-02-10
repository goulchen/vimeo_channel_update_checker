#!/bin/sh
docker build -t check_vimeo_changes .
docker rm --force check_vimeo_changes
docker run --name check_vimeo_changes -a stdin -a stdout -a stderr check_vimeo_changes


