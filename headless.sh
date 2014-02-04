#!/bin/sh
xvfb-run --server-args="-screen 0, 1920x1080x24" --auto-servernum nosetests -sv --logging-level=ERROR --with-xunit $@

#or
#Xvfb :2 -screen 0 1920x1080x24 &
#DISPLAY=:2 nosetests -sv --logging-level=ERROR
