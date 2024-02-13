#!/home/username/parrot/bin/python
from __future__ import division
import cv2 as cv
import argparse


alpha_slider_max = 100
title_window = 'Linear Blend'

def on_trackbar(val):
    img = cv.imread("/home/accurpress/catkin_ws/src/deep_drone/repo/frames/pid_.png")
    cv.imshow(title_window, img)


parser = argparse.ArgumentParser(description='Code for Adding a Trackbar to our applications tutorial.')
parser.add_argument('--input1', help='Path to the first input image.', default='/home/accurpress/catkin_ws/src/deep_drone/repo/frames/img_sphinx.jpg')
parser.add_argument('--input2', help='Path to the second input image.', default='/home/accurpress/catkin_ws/src/deep_drone/repo/frames/img_sphinx.jpg')

args = parser.parse_args()

src1 = cv.imread(cv.samples.findFile(args.input1))
src2 = cv.imread(cv.samples.findFile(args.input2))

if src1 is None:
    print('Could not open or find the image: ', args.input1)
    exit(0)
if src2 is None:
    print('Could not open or find the image: ', args.input2)
    exit(0)


cv.namedWindow(title_window)
trackbar_name = 'Alpha x %d' % alpha_slider_max
cv.createTrackbar(trackbar_name, title_window , 0, alpha_slider_max, on_trackbar)
# Show some stuff
on_trackbar(0)
# Wait until user press some key
cv.waitKey()