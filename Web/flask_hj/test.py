# from flask import Flask,url_for, render_template, Response
# from darkflow.net.build import TFNet
# import cv2
# import tensorflow as tf
#
#
# app=Flask(__name__)
#
# options = {"model": "cfg/yolo.cfg", "load": "bin/yolo.weights", "threshold": 0.1}
#
# tfnet = TFNet(options)
#
# def gen(camera):
#
#     sess = tf.Session()
#
#     with sess.as_default():
#
#         while True:
#
#             success, img = camera.read()
#
#             if success:
#                 try:
#                     results = tfnet.return_predict(img)
#
#                     for result in results:
#                         tl= (result['topleft']['x'],result['topleft']['y'])
#                         br =(result['bottomright']['x'],result['bottomright']['y'])
#                         label = result['label']
#                         cv2.rectangle(img,tl,br,(0,255,0),3)
#                         cv2.putText(img,label,br,cv2.FONT_HERSHEY_COMPLEX, 2,(0,0,0),1)
#                         print(label)
#
#                     ret, jpeg = cv2.imencode('.jpg', img)
#                     frame = jpeg.tobytes()
#
#                     yield (b'--frame\r\n'
#                            b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
#                 except:
#                   print("An exception occurred")
#
#             else:
#                 print("Status of camera.read()\n",success, img,"\n=======================")
#
#
#
# @app.route('/video_feed')
# def video_feed():
#     camera = cv2.VideoCapture(0)
#     return Response(gen(camera), mimetype='multipart/x-mixed-replace; boundary=frame')
#
# @app.route('/')
# def webcam():
#     return render_template('webcam.html')

from darkflow.net.build import TFNet
import cv2

options = {"model": "cfg/yolo.cfg", "load": "bin/yolo.weights", "threshold": 0.1}
tfnet = TFNet(options)

imgcv = cv2.imread("./sample_img/sample_dog.jpg")
result = tfnet.return_predict(imgcv)
print(result)


[{'label': 'bicycle', 'confidence': 0.84797806, 'topleft': {'x': 80, 'y': 113}, 'bottomright': {'x': 555, 'y': 467}}, {'label': 'motorbike', 'confidence': 0.29457858, 'topleft': {'x': 59, 'y': 76}, 'bottomright': {'x': 113, 'y': 124}}, {'label': 'truck', 'confidence': 0.80142015, 'topleft': {'x': 462, 'y': 81}, 'bottomright': {'x': 694, 'y': 167}}, {'label': 'cat', 'confidence': 0.124768995, 'topleft': {'x': 139, 'y': 197}, 'bottomright': {'x': 313, 'y': 551}}, {'label': 'dog', 'confidence': 0.77081436, 'topleft': {'x': 136, 'y': 214}, 'bottomright': {'x': 322, 'y': 539}}]
