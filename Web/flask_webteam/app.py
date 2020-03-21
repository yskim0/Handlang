from flask import Flask, url_for, render_template, Response, request, jsonify
from darkflow.net.build import TFNet
import cv2
import tensorflow as tf
import json

app = Flask(__name__)

options = {"model": "cfg/yolo.cfg", "load": "bin/yolo.weights", "threshold": 0.4}

tfnet = TFNet(options)

# 실시간으로 detect 된 label
predict_label = ''

def get_alphabet_list():
    alphabet_list = ['person', 'teddybear', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o',
                     'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

    return alphabet_list


def alphabet_list_idx(element):
    next_topic = ""
    previous_topic = ""

    alphabet_list = get_alphabet_list()

    list_idx_end = len(alphabet_list) - 1  # 마지막 인덱스
    idx_now = alphabet_list.index(element)

    if idx_now == list_idx_end:
        next_topic = alphabet_list[0]
    else:
        next_topic = alphabet_list[idx_now + 1]

    if idx_now != 0:
        previous_topic = alphabet_list[idx_now - 1]

    return next_topic, previous_topic


def gen(camera):
    if not camera.isOpened():
        raise RuntimeError("Could not start camera")

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
                        confidence = result['confidence']

                        cv2.rectangle(img, tl, br, (0, 255, 0), 3)
                        cv2.putText(img, label, br, cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 2)

                        global predict_label
                        predict_label = label

                    ret, jpeg = cv2.imencode('.jpg', img)
                    frame = jpeg.tobytes()

                    yield (b'--frame\r\n'
                           b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
                except:
                    print("An exception occurred")

            else:
                print("Status of camera.read()\n", success, "\n=======================")


# for ajax
@app.route('/return_label', methods=['POST', 'GET'])
def return_label():
    global predict_label

    value = request.form.get("target", False)

    predict_label = " " + predict_label.upper() + " "  # ajax 에서 값 받아올때 공백이 앞뒤로 붙는데 python strip() 함수가 안먹어서 일단 임시방편으로

    if predict_label == '':
        predict_result = {
            'status': 0,
            'info': 'not detected',
            'label': ''
        }
    elif predict_label != value:
        predict_result = {
            'status': 0,
            'info': '틀렸습니다😭',
            'label': predict_label
        }
        print("틀림!")
    else:
        predict_result = {
            'status': 1,
            'info': '맞았습니다!',
            'label': predict_label
        }

    # result 의 status 값이 1이면 참 -> main.js 에서 correct 값 증가

    json_data = json.dumps(predict_result)  # json 형태로 바꿔줘야 에러 안남
    return json_data


@app.route('/quiz')
def quiz():
    return render_template('quiz.html')


@app.route('/practice_asl')
def practice_asl():
    alphabet_list = get_alphabet_list()
    return render_template('practice_asl.html', alphabet_list=alphabet_list)


# video streaming
@app.route('/video_feed')
def video_feed():
    camera = cv2.VideoCapture(0)
    return Response(gen(camera), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/practice', methods=['GET', 'POST'])
def practice():
    element = request.args.get('element')
    alphabet = element.upper()
    img = "../static/img/asl_" + element + ".png"

    next_topic, previous_topic = alphabet_list_idx(element)

    return render_template('practice.html', img=img, alphabet=alphabet, previous_topic=previous_topic,next_topic=next_topic)


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
