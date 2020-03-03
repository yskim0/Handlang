from flask import Flask, url_for, render_template, Response
from darkflow.net.build import TFNet
import cv2
import tensorflow as tf
import threading
import numpy as np

options = {"model": "./cfg/handlang-small.cfg",
           "pbLoad": "./darkflow/built_graph/handlang-small.pb",
           "metaLoad": './darkflow/built_graph/handlang-small.meta' , "threshold": 0.1}
tfnet = TFNet(options)

imgcv = cv2.imread("n_34_rotate_2.jpeg")
result = tfnet.return_predict(imgcv)
print(result)