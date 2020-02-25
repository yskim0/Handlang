from flask import Flask, url_for, render_template, Response
from darkflow.net.build import TFNet
import cv2
import tensorflow as tf

app = Flask(__name__)
options = {"model": "./cfg/handlang-small.cfg",
           "pbload": "./build-graph/handlang-small.pb",
           "metaLoad":"./build-graph/handlang-small.meta",
           "threshold": 0.2}
tfnet = TFNet(options)


def gen(camera):
    sess = tf.Session()

    with sess.as_default():

        while True:

            success, img = camera.read()

            if success:
                try:
                    results = tfnet.return_predict(img)

                    for result in results:
                        tl = (result['topleft']['x'], result['topleft']['y'])
                        br = (result['bottomright']['x'], result['bottomright']['y'])
                        label = result['label']
                        cv2.rectangle(img, tl, br, (0, 255, 0), 3)
                        cv2.putText(img, label, br, cv2.FONT_HERSHEY_COMPLEX, 2, (0, 0, 0), 1)
                    cv2.imshow('frame',img)

                    ret, jpeg = cv2.imencode('.jpg', img)
                    frame = jpeg.tobytes()

                    yield (b'--frame\r\n'
                           b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
                except:
                    print("An exception occurred")

            else:
                print("Status of camera.read()\n", success, img, "\n=======================")
@app.route('/video_feed')
def video_feed():
    cam = cv2.VideoCapture(0)
    return Response(gen(cam),mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/')
def webcam():
    return render_template('webcam.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False)