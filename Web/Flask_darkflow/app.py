import sys
import fcntl
import cv2
from darkflow.net.build import TFNet
import numpy as np
import time


# load the trained model which is stord as .pb and .meta
# options= {"pbLoad": "built_graph/tiny-yolo-voc-person.pb", "metaLoad": "built_graph/tiny-yolo-voc-person.meta",
#           "threshold": 0.45, "gpu": 0.5}

options = {"model": "cfg/yolo.cfg", "load": "bin/yolo.weights", "threshold": 0.45}
          
tfnet = TFNet(options)

capture = cv2.VideoCapture(0) # using web camera


while (capture.isOpened()):
    stime=time.time()
    ret,frame=capture.read()
    result=tfnet.return_predict(frame)
    
    if ret:
        for result in result:
            tl= (result['topleft']['x'],result['topleft']['y'])
            br =(result['bottomright']['x'],result['bottomright']['y'])
            label = result['label']
            frame=cv2.rectangle(frame,tl,br,(0,255,0),7)
            frame =cv2.putText(frame,label,br,cv2.FONT_HERSHEY_COMPLEX, 10,(0,0,0),2)
        cv2.imshow('frame',frame)
        
        print('FPS{:.1f}'.format(1/(time.time() -stime)))
        if cv2.waitKey(1)& 0xff ==ord('q'):
            break

capture.release()
cv2.destroyAllWindows()