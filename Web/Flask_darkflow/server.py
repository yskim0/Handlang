from flask import Flask, url_for, render_template, Response
from darkflow.net.build import TFNet
import cv2
import tensorflow as tf
import threading
import numpy
import sys
from PIL import Image

app = Flask(__name__)

# ajax 통신 변수
tem_message = "temporary"
final_message = "prediction result"


# 손 detect 모델
options_hand = {"model": "./cfg/yolo-hands.cfg", "load": "./bin/yolo-hand-detect.weights", "threshold": 0.4}

tfnet_hand = TFNet(options_hand)


# 수화번역 model
options_signLanguage = {"model": "./cfg/handlang-small.cfg",
                       "pbLoad": "./darkflow/built_graph/handlang-small.pb",
                       "metaLoad": './darkflow/built_graph/handlang-small.meta' , "threshold": 0.07}
tfnet_detect = TFNet(options_signLanguage)

def gen(camera):
    sess = tf.Session()
    with sess.as_default():
        while True:
            success, img = camera.read()
            if success:
                    results = tfnet_hand.return_predict(img)

                    for result in results:

                        if result["label"]: # 만일 hand detect 된다면

                            label = result["label"] # hand detect 예측값
                            confidence = result["confidence"] # hand detect 신뢰도

                            cropped_img = cv2.rectangle(img,
                                        (result["topleft"]["x"]-20, result["topleft"]["y"]-80),
                                        (result["bottomright"]["x"]+20, result["bottomright"]["y"]+60),
                                        (255, 0, 0), 4)

                            text_x, text_y = result["topleft"]["x"], result["topleft"]["y"] # 결과 쓸 위치

                            hand_label = ""
                            if cropped_img.shape[0]*cropped_img.shape[1]: # hand detect 만 cropped 된 img 가 크기가 0이 아니면
                                
                                print("(cropped img 성공)")

                                hand_results = tfnet_detect.return_predict(cropped_img)
                                if hand_results: # 수화 예측값이 나온다면

                                    hand_label = hand_results[0]["label"]
                                    hand_confidence = hand_results[0]["confidence"]
                                else:
                                    print("*** cropped img predict 실패 ***")


                            if hand_label != "": # 수화 예측값이 나온다면
                                print("== 수화 preditct 성공 ==")

                                cv2.putText(cropped_img, hand_label, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX,
                                            0.8, (0, 255, 0), 2, cv2.LINE_AA)

                                print("result: ", hand_label, "| confidence: ", hand_confidence)

                            else: # only hand detected

                                cv2.putText(cropped_img, "hand", (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX,
                                            0.8, (0, 255, 0), 2, cv2.LINE_AA)
                            
                            # 예측값이랑 신뢰도 같이 프린트해서 보여주기 (기존 것 위에 계속 출력)
                            global tem_message
                            tem_message = hand_label # 수화 디텍트 안되면 ""
                                

                    #cv2.imshow('frame',img)

                    ret, jpeg = cv2.imencode('.jpg', img)
                    frame = jpeg.tobytes()

                    yield (b'--frame\r\n'
                           b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

            else:
                print("Status of camera.read()\n", success, img, "\n=======================")

# ajax 통신 함수
@app.route("/sendResult")
def sendResult():
    global tem_message, final_message

    if tem_message == "temporary":
        final_message = "no prediction yet"

    else:
        final_message = tem_message

    return final_message

@app.route('/video_feed')
def video_feed():
    cam = cv2.VideoCapture(0)
    return Response(gen(cam), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/')
def webcam():
    return render_template('webcam.html', resultReceived=sendResult())

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
