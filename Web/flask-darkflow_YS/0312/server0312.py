from flask import Flask, url_for, render_template, Response, abort, Blueprint
from jinja2 import TemplateNotFound
from darkflow.net.build import TFNet
import cv2
import tensorflow as tf

app = Flask(__name__, static_url_path='/static')

options = {"model": "./cfg/handlang-small.cfg",
           "metaLoad": "./darkflow/built_graph/handlang-small.meta",
           "pbLoad": './darkflow/built_graph/handlang-small.pb', "threshold": 0.4}

# options = {"model": "./cfg/yolo.cfg", "load": "./bin/yolov2.weights", "threshold": 0.4}

tfnet = TFNet(options)

predict_label = ''


def gen(camera):
    sess = tf.Session()

    with sess.as_default():

        while True:

            success, img = camera.read()

            if success:
                results = tfnet.return_predict(img)

                for result in results:
                    label = result["label"]
                    # print(label)

                    cv2.rectangle(img,
                                  (result["topleft"]["x"], result["topleft"]["y"]),
                                  (result["bottomright"]["x"], result["bottomright"]["y"]),
                                  (255, 0, 0), 4)
                    text_x, text_y = result["topleft"]["x"] - 10, result["topleft"]["y"] - 10
                    cv2.putText(img, label, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX,
                                0.8, (0, 255, 0), 2, cv2.LINE_AA)

                    global predict_label
                    predict_label = label

                # cv2.imshow('frame', img)

                ret, jpeg = cv2.imencode('.jpg', img)
                frame = jpeg.tobytes()

                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
            else:
                print("Status of camera.read()\n", success, img, "\n=======================")



@app.route('/video_feed')
def video_feed():
    cam = cv2.VideoCapture(0)
    return Response(gen(cam), mimetype='multipart/x-mixed-replace; boundary=frame')

#
@app.route('/')
def webcam():
    # return render_template('webcam.html', return_label = return_label())
    # return render_template('webcam-0.html')
    return render_template('index.html')

@app.route('/charstudy')
def charstudy():
    return render_template('charstudy.html')


@app.route('/quiz')
def quiz():
    return render_template('quiz.html')


@app.route('/numstudy')
def numstudy():
    return render_template('numstudy.html')


@app.route('/selectChar')
def selectChar():
    return render_template('selectChar.html')

@app.route('/return_label')
def return_label():
    global predict_label, final_msg
    if predict_label == '':
        final_msg = 'not detected'
        return final_msg
    return predict_label


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False)
