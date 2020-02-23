from flask import Flask, url_for, render_template, Response
import threading
import numpy
import cv2, time
from darkflow.net.build import TFNet
from yolo_video import yoloCamera as camera
import tensorflow as tf

app = Flask(__name__)

options = {"model": "cfg/handlang-small.cfg",            
           "pbLoad": 'darkflow/built_graph/handlang-small.pb', 
           "metaLoad": 'darkflow/built_graph/handlang-small.meta' , "threshold": 0.1}

tfnet = TFNet(options)

def gen(camera):
    sess = tf.Session()

    with sess.as_default():

        while True:
            success, img = camera.read()
            
            results = tfnet.return_predict(img)         
            for result in results:
                tl= (result['topleft']['x'],result['topleft']['y'])
                br =(result['bottomright']['x'],result['bottomright']['y'])
                label = result['label']
                cv2.rectangle(img,tl,br,(0,255,0),3)
                cv2.putText(img,label,br,cv2.FONT_HERSHEY_COMPLEX, 2,(0,0,0),1)
            # cv2.imshow('frame',img)
                
            ret, jpeg = cv2.imencode('.jpg', img) 
            frame = jpeg.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    cam = cv2.VideoCapture(0)
    # cam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    # cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 360)
    return Response(gen(cam),mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/')
def webcam():
    return render_template('webcam.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False)