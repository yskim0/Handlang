# ajax 코드
from flask import Flask,url_for, render_template, Response
from darkflow.net.build import TFNet
import cv2
import tensorflow as tf

app=Flask(__name__)

options = {"model": "cfg/yolo.cfg", "load": "bin/yolo.weights", "threshold": 0.4}

tfnet = TFNet(options)

#실시간으로 detection된 label
current_label = ""

#최종 출력 결과 저장
final_result = ""

#split 이거 기준으로 jquery에서 split 
split = "2020HANDLANG"

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
                        tl= (result['topleft']['x'],result['topleft']['y'])
                        br =(result['bottomright']['x'],result['bottomright']['y'])
                        label = result['label']
                        confidence = result['confidence']
                        
                        global current_label

                        if confidence > 0.4: # 신뢰도가 0.4 이상일 경우만
                            current_label += label
                            current_label += split

                        print(label)

                        cv2.rectangle(img,tl,br,(0,255,0),3)
                        cv2.putText(img,label,br,cv2.FONT_HERSHEY_COMPLEX, 1,(0,0,0),2)
                    
                    ret, jpeg = cv2.imencode('.jpg', img)
                    frame = jpeg.tobytes()

                    yield (b'--frame\r\n'
                           b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
                except:
                  print("An exception occurred")

            else:
                print("Status of camera.read()\n",success,"\n=======================")


#for ajax
@app.route('/getlabel')
def getLabel():
    global current_label
    global final_result
    final_result = current_label
    current_label = "" # 초기화
    return final_result


@app.route('/eraselabel')
def eraseLabel():
    global final_result
    global current_label
    current_label = "" # 초기화
    final_result = "" # 초기화
    return final_result

#video streaming
@app.route('/video_feed')
def video_feed():
    camera = cv2.VideoCapture(0)
    return Response(gen(camera), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def webcam():
    return render_template('webcam_2.html')

if __name__=="__main__":
    app.run(host='0.0.0.0', port=5000,debug=True)
