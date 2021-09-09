from imutils.video import VideoStream
import imagezmq
import argparse
import socket
import time


# constructs argument parser
ap = argparse.ArgumentParser()
ap.add_argument("-s", "--server-ip", required=True,
                help="ip address of server to which the client will connect")
args = vars(ap.parse_args())

# initializes imagesender object with server socket
sender = imagezmq.ImageSender(connect_to="tcp://{}:5555".format(
    args["server_ip"]))

print("Connection to Server Established")

# get host name, initialize video stream, allow sensor to warm up
rpiName = socket.gethostname()
vs = VideoStream(src=0).start()

print("Starting Video Stream")

time.sleep(2.0)

while True:
    frame = vs.read()
    sender.send_image(rpiName, frame)
        

    # cv.imshow("frame", frame)
    # cv.waitKey(1)
