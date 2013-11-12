#!/bin/sh
#DISPLAY=:2 xvfb-run --auto-servernum --server-num=0 python manage.py -cu 30

#or
Xvfb :2 -screen 0 1024x768x24 &
DISPLAY=:2 python manage.py -cu 30
