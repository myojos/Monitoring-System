# Motion Detector

import cv2, time, pandas
from datetime import datetime
import os
from camera import Camera
import glob

DIFF_THRESHOLD = 30
SIZE = (256, 256)


class MotionDetection:
    def __init__(self, room_name):
        self.static_back = None
        self.motion_list = [0, 0]
        self.times = []
        self.room = Camera(room_name)
        self.room_name = room_name
        self.images = []

    def add_image(self, img_path):
        frame = cv2.imread(img_path)
        frame = cv2.resize(frame, SIZE)
        # gray and blur to detect difference
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)

        # first image
        if self.static_back is None:
            self.static_back = gray
            return

        # compute difference
        diff_frame = cv2.absdiff(self.static_back, gray)
        thresh_frame = cv2.threshold(diff_frame, DIFF_THRESHOLD, 255, cv2.THRESH_BINARY)[1]
        thresh_frame = cv2.dilate(thresh_frame, None, iterations=2)
        self.static_back = gray

        # Finding contour
        # TODO tell Jonathan
        cnts, _ = cv2.findContours(thresh_frame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        motion = 0
        for contour in cnts:
            if cv2.contourArea(contour) < 1000:
                continue
            motion = 1
            (x, y, w, h) = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)

        # Appending current motion
        self.motion_list.append(motion)
        if not motion:
            os.remove(img_path)
        else:
            cv2.imwrite(img_path, frame)
            self.room.check(img_path, frame)
            self.images.append(img_path)

        # Detect start and end motion
        motion_list = self.motion_list[-2:]
        if motion_list[-1] == 1 and motion_list[-2] == 0:
            self.times.append(datetime.now())
        if motion_list[-1] == 0 and motion_list[-2] == 1:
            self.times.append(datetime.now())

        # convert to videos
        if len(self.images) >= 30:
            imgs = []
            for im_file in self.images:
                imgs.append(cv2.imread(im_file))
                os.remove(im_file)
            out = cv2.VideoWriter('detected-{room}-{time}.avi'
                                  .format(room=self.room_name, time='now'),
                                  cv2.VideoWriter_fourcc(*'DIVX'), 4, SIZE)
            for img in imgs:
                out.write(img)
            out.release()
            self.images.clear()
