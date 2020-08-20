#Note: use this command to run this py file
# python alert_system.py --prototxt our_model.prototxt.txt --model our_model.caffemodel

from imutils.video import VideoStream
from imutils.video import FPS
import numpy as np
import argparse
import imutils
from imutils import paths
import threading 
import os 
import time
from sinchsms import SinchSMS
import smtplib 
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.mime.base import MIMEBase 
from email import encoders 
#from sonar import se
from playsound import playsound
import cv2
number = '+91XXXXXXXXXX'
message = 'Object detected'
c = 0
client = SinchSMS('', '')
#############################################################################################
fromaddr = "XXX@gmail.com"
toaddr = "YYY@gmail.com"
msg = MIMEMultipart()   
msg['From'] = fromaddr 
msg['To'] = toaddr 
msg['Subject'] = "Obstracle detection"
body = "Body_of_the_mail"
msg.attach(MIMEText(body, 'plain')) 
#################################################################################
def email():

	filename = "proof1.png"
	attachment = open("proof1.png", "rb") 
	p = MIMEBase('application', 'octet-stream') 
	p.set_payload((attachment).read()) 
	encoders.encode_base64(p) 
	p.add_header('Content-Disposition', "attachment; filename= %s" % filename) 
	msg.attach(p) 
	s = smtplib.SMTP('smtp.gmail.com', 587) 
	s.starttls() 
	s.login('rethinadurai@gmail.com', "durai durai") 
	text = msg.as_string() 
	s.sendmail(fromaddr, toaddr, text) 
	s.quit() 
######################################################
def sms():
	print("Sending '%s' to %s" % (message, number))
	response = client.send_message(number, message)
	message_id = response['messageId']
	response = client.check_status(message_id)
#######################################################
def start():
	t1 = threading.Thread(target=sms, name='t1') 
	t2 = threading.Thread(target=email, name='t2')
	#t3 = threading.Thread(target=play, name='t3') 
	t1.start() 
	#t1.join() 
	t2.start()
#####################################################
def join():
	t1.join() 
	#t2.join() 
	#t3.join()


###################################################




CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
	"bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
	"dog", "horse", "motorbike", "person", "pottedplant", "sheep",
	"sofa", "train", "tvmonitor"]
COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))


print("[INFO] loading model...")
net = cv2.dnn.readNetFromCaffe("our_model.prototxt.txt", "our_model.caffemodel")


print("[INFO] starting video stream...")
vs = VideoStream(src=1).start()
time.sleep(2.0)
fps = FPS().start()


while True:

	frame = vs.read()
	if(frame is not None):
		frame = imutils.resize(frame, width=400)
		c +=1
		if(c==30):
			break 
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

				#elif d == "sofa" or "tvmonitor":
#
#					e = "building"
#
#					cv2.putText(frame, e, (startX, y),
#						cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2)
#					cv2.rectangle(frame, (startX, startY), (endX, endY),
#						COLORS[idx], 2)
#
#				elif d == "pottedplant":
#
#					f = "tree"
#				cv2.putText(frame, f, (startX, y),
#						cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2)
#
#					cv2.rectangle(frame, (startX, startY), (endX, endY),
#						COLORS[idx], 2)

				else:
					label = "obstacle"

					cv2.putText(frame, label, (startX, y),
						cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2)
				cv2.imwrite("proof1.png",frame)
				start()	
				playsound('a.mp3')

		#cv2.imshow("Frame", frame)
		key = cv2.waitKey(1) & 0xFF
	else:
		print("Signal lost")
		break


	if key == ord("q"):
		break

	#fps.update()
fps.stop()
print("[INFO] elapsed time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))


cv2.destroyAllWindows()
vs.stop()
