import zmq
import datetime
import time
import threading

from flask import Response
from flask import Flask
from flask import render_template

import numpy as np
import imagezmq
import argparse
import imutils
import cv2 as cv

# mac ip : 192.168.0.13
# windows ip : 192.168.0.21

imageHub = imagezmq.ImageHub()

outputFrame = None

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


def get_frames():
    global outputFrame

    while True:
        frame = imageHub.recv_image(zmq.NOBLOCK)[1]
        imageHub.send_reply(b'OK')

        frame = imutils.resize(frame, width=400)
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        gray = cv.GaussianBlur(gray, (7, 7), 0)

        timestamp = datetime.datetime.now()
        cv.putText(frame, timestamp.strftime(
            "%A %d %B %Y %I:%M:%S%p"), (10, frame.shape[0] - 10),
                   cv.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)

        outputFrame = frame.copy()

        (flag, encodedImage) = cv.imencode(".jpg", outputFrame)

        if not flag:
            continue

        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
                bytearray(encodedImage) + b'\r\n')


@app.route("/video_feed")
def video_feed():
    return Response(get_frames(),
                    mimetype="multipart/x-mixed-replace; boundary=frame")


app.run(host="192.168.0.21", port=8000, debug=True,
        threaded=True, use_reloader=False)
