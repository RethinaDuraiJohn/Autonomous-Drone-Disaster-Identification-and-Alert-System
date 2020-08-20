
# python main.py --prototxt MobileNetSSD_deploy.prototxt.txt --model MobileNetSSD_deploy.caffemodel

from imutils.video import VideoStream
from imutils.video import FPS
import numpy as np
import argparse
import imutils
from imutils import paths
import time
#from sonar import se
from playsound import playsound
import cv2





CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
	"bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
	"dog", "horse", "motorbike", "person", "pottedplant", "sheep",
	"sofa", "train", "tvmonitor"]
COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))


print("[INFO] loading model...")
net = cv2.dnn.readNetFromCaffe("MobileNetSSD_deploy.prototxt.txt", "MobileNetSSD_deploy.caffemodel")


print("[INFO] starting video stream...")
vs = VideoStream(src=0).start()
time.sleep(2.0)
fps = FPS().start()


while True:

	frame = vs.read()
	frame = imutils.resize(frame, width=400)

	(h,w) = frame.shape[:2]
	blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)),
		0.007843, (300, 300), 127.5)


	net.setInput(blob)
	detections = net.forward()


	for i in np.arange(0, detections.shape[2]):
		confidence = detections[0, 0, i, 2]


		if confidence > 0.5:

			idx = int(detections[0, 0, i, 1])
			box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
			(startX, startY, endX, endY) = box.astype("int")
			#height = endY-startY

			label = "{}: {:.2f}%".format(CLASSES[idx],
				confidence * 100)
			y = startY - 15 if startY - 15 > 15 else startY + 15
			d=label[0:-8]

			#se()
			if d == "bird":
				cv2.putText(frame, d, (startX, y),
					cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2)
				#playsound("a.mp3")
				cv2.rectangle(frame, (startX, startY), (endX, endY),
					COLORS[idx], 2)

			elif d == "person":


				cv2.putText(frame, d, (startX, y),
					cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2)
				#playsound("a.mp3")
				cv2.rectangle(frame, (startX, startY), (endX, endY),
					COLORS[idx], 2)


			elif d == "pottedplant":

				f = "tree"

				cv2.putText(frame, f, (startX, y),
					cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2)

				cv2.rectangle(frame, (startX, startY), (endX, endY),
					COLORS[idx], 2)

			else:
				label = "obstacle"

				cv2.putText(frame, label, (startX, y),
					cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2)

	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF


	if key == ord("q"):
		break

	fps.update()
fps.stop()
print("[INFO] elapsed time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))


cv2.destroyAllWindows()
vs.stop()
