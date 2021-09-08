import zmq
from imutils import build_montages
from datetime import datetime
import time

import numpy as np
import imagezmq
import argparse
import imutils
import cv2 as cv

# server ip : 10.19.48.109

imageHub = imagezmq.ImageHub()

frame_count = 0

time_start = time.time()

while True:

    (rpiName, frame) = imageHub.recv_image(zmq.NOBLOCK)
    imageHub.send_reply(b'OK')

    if frame_count == 60:
        time_end = time.time()
        fps = 60/(time_end - time_start)

        print("FPS is {}".format(fps))

    frame_count += 1

    print(frame_count)

    cv.imshow("frame", frame)
    cv.waitKey(1)





