import os
import time
from models.people_counter.pyimagesearch.centroidtracker import CentroidTracker
from models.people_counter.pyimagesearch.trackableobject import TrackableObject
import numpy as np
import dlib
import cv2

CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
           "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
           "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
           "sofa", "train", "tvmonitor"]

PEOPLE_DIR = 'people_counter'
MODEL_DIR = 'mobilnet_ssd'
CAFFE_MODEL = 'MobileNetSSD_deploy.caffemodel'
PROTO_MODEL = 'MobileNetSSD_deploy.prototxt'
SIZE = (256, 256)
CONFIDENCE = 0.7


class People():
    def __init__(self, constraints):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        people_path = os.path.join(dir_path, PEOPLE_DIR)
        model_path = os.path.join(people_path, MODEL_DIR)
        caffe_path = os.path.join(model_path, CAFFE_MODEL)
        proto_path = os.path.join(model_path, PROTO_MODEL)
        self.net = cv2.dnn.readNetFromCaffe(proto_path, caffe_path)
        self.ct = CentroidTracker(maxDisappeared=40, maxDistance=50)
        # self.trackers = []
        # self.trackableObjects = {}
        # totalFrames = 0
        # totalDown = 0
        # totalUp = 0
        self.min = 0
        self.max = 1e9
        for constrain_name in constraints:
            constraints_value = constraints[constrain_name]
            if constrain_name == 'min':
                self.min = constraints_value
            elif constrain_name == 'max':
                self.max = constraints_value
            else:
                print('Unsupported constrain {cname} for People model'.format(cname=constrain_name))

    def check(self, img_path, frame):
        # rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        rects = []
        blob = cv2.dnn.blobFromImage(frame, 0.007843, SIZE, 127.5)
        self.net.setInput(blob)
        detections = self.net.forward()

        count = 0
        # loop over the detections
        for i in np.arange(0, detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            if confidence >= CONFIDENCE:
                cidx = int(detections[0, 0, i, 1])
                if CLASSES[cidx] != "person":
                    continue
                count += 1
        return count < self.min or count > self.max
