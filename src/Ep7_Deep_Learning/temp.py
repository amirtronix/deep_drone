#!/home/username/parrot/bin/python

import torch
from pathlib import Path
from PIL import Image
import matplotlib.pyplot as plt

model = torch.hub.load('ultralytics/yolov5', 'yolov5m')

import cv2
import numpy as np

# Load image
im = '/home/accurpress/catkin_ws/src/deep_ros/repo/frames/2023-11-15T15:30:55/img_0191.jpg'  #

# Perform inference
results = model(im)

cv2.imshow('Screen', cv2.cvtColor(results.render()[0], cv2.COLOR_BGR2RGB))

cv2.waitKey(2000)