from datetime import datetime
import threading

import numpy as np
import imagezmq
import argparse
import imutils
import cv2 as cv

# server ip : 10.19.48.109


imageHub = imagezmq.ImageHub()


def get_frame():
    frame = imageHub.recv_image()[1]
    imageHub.send_reply(b'OK')
    cv.imshow("frame", frame)
    cv.waitKey(1)


while True:

    frame1 = threading.Thread(target=get_frame)
    frame2 = threading.Thread(target=get_frame)

    frame1.start()
    frame2.start()

    frame1.join()
    frame2.join()


    #cv.imshow("frame", frame2)
    #cv.waitKey(1)


