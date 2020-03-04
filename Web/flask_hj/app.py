#real code
from flask import Flask,url_for, render_template, Response
from darkflow.net.build import TFNet
import cv2
import tensorflow as tf


app=Flask(__name__)

options = {"model": "cfg/yolo.cfg", "load": "bin/yolo.weights", "threshold": 0.1}

tfnet = TFNet(options)

label1=""

def gen(camera):
    if not camera.isOpened():
        raise RuntimeError("Could not start camera")
    output="sentence: "
    # label_before=''

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
                        global label1
                        label1=label
                        print(label)
                        output+=label
                        cv2.rectangle(img,tl,br,(0,255,0),3)
                        cv2.putText(img,label,br,cv2.FONT_HERSHEY_COMPLEX, 2,(0,0,0),1)
                    cv2.putText(img,output,(20,35), cv2.FONT_HERSHEY_SIMPLEX, 0.5,(255,255,255),1)
                    ret, jpeg = cv2.imencode('.jpg', img)
                    frame = jpeg.tobytes()

                    yield (b'--frame\r\n'
                           b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
                except:
                  print("An exception occurred")

            else:
                print("Status of camera.read()\n",success, img,"\n=======================")

#label을 저장해서 불러오기
# def detection(vid):


#for ajax
@app.route('/getlabel')
def getLabel():
    global label1
    return label1




@app.route('/video_feed')
def video_feed():
    camera = cv2.VideoCapture(0)
    return Response(gen(camera), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def webcam():
    return render_template('webcam.html')

if __name__=="__main__":
    app.run(host='127.0.0.1', port=5000,debug=True)
