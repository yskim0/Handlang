from flask import Flask, url_for, render_template, Response
from darkflow.net.build import TFNet
import cv2
import tensorflow as tf
import threading
import numpy


app = Flask(__name__)

options = {"model": "./cfg/handlang-small.cfg",
           "pbLoad": "./darkflow/built_graph/handlang-small.pb",
           "metaLoad": './darkflow/built_graph/handlang-small.meta' , "threshold": 0.4}
tfnet = TFNet(options)


def gen(camera):
    sess = tf.Session()

    with sess.as_default():

        while True:

            success, img = camera.read()

            if success:
                    results = tfnet.return_predict(img)


                    for result in results:
                        #tl = (result["topleft"]['x'], result['topleft']['y'])
                        #br = (result['bottomright']['x'], result['bottomright']['y'])
                        label = result["label"]
                        print(label)
                        cv2.rectangle(img,
                                    (result["topleft"]["x"], result["topleft"]["y"]),
                                    (result["bottomright"]["x"], result["bottomright"]["y"]),
                                    (255, 0, 0), 4)
                        text_x, text_y = result["topleft"]["x"] - 10, result["topleft"]["y"] - 10
                        cv2.putText(img, result["label"], (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX,
                                    0.8, (0, 255, 0), 2, cv2.LINE_AA)
                    cv2.imshow('frame',img)

                    ret, jpeg = cv2.imencode('.jpg', img)
                    frame = jpeg.tobytes()

                    yield (b'--frame\r\n'
                           b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
            else:
                print("Status of camera.read()\n", success, img, "\n=======================")
@app.route('/video_feed')
def video_feed():
    cam = cv2.VideoCapture(0)
    # cam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    # cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 360)
    #if cam.isOpened():
    #    print('opended')
    return Response(gen(cam),mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/')
def webcam():
    return render_template('webcam.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False)