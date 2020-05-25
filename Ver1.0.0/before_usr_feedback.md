## Our Challenges Before User Feedback

The feedback we received was mainly related to the accuracy of the model, so we prioritized improving the model's performance.

## about models


1. YOLO darknet

YOLO is the model with excellent performance in Object detection.
We used darkflow, not yolo darknet, to take advantage of tensorflow.

https://github.com/thtrieu/darkflow


The most attempts were made at darkflow.

- YOLO_experiment_1
    - [a~z] 600 images each. training 500 epochs
    - acc : 0.42


**Feedback -> Predict performance is poor.**

-----

- YOLO_experiment_2
    - pretrained weight - hand tracking model (https://github.com/Abdul-Mukit/dope_with_hand_tracking)
    - [a~y](excluding `j`) 600 images each. 140 epochs
    - acc : 0.47
    - ![047](/img/47.png/)


- YOLO_experiment_3
    - pretrained weight - yolov2-tiny.weight(https://pjreddie.com/darknet/yolov2/)
    - [a~y](excluding `j`) 600 images each. 220 epochs
    - acc : 0.56
    - ![056](/img/56.png)


**Feedback -> It is still not a satisfactory performance.**


----


2. Inception-v3

We tried transfer learning by using `inception-v3`.

- [a~y](excluding `j`) 600 images each. 1000 steps
- test acc. : about 88%
    - but not that much at real-time...
    - ![088](/img/88.png)


3. Tensorflow-Object-Detection-API

We tried transfer learning by using `fast r-cnn`.
- [a~y](excluding `j`) 600 images each. 6000 steps
- test acc. : about 80%
    - not test by images, but test by webcam.
        - poor performance


**Self-feedback: It is still not a satisfactory performance.**

----

4. Finally Custom CNN model(our current model)!

**Feedback : Great Prediction!**

----


## about Web

The feedback said that it would be good to have a quiz, so we made a quiz that can test after learning oneself.


![quiz](/img/quiz.png)