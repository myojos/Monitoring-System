import os
import argparse
from multiprocessing import Process
import time
import subprocess
from motion_detection import MotionDetection

ADB_PATH = 'C:\\Users\\khale\\AppData\\Local\\Android\\Sdk\\platform-tools\\adb.exe'
IMG_DIR = 'imgs'
VID_DIR = 'videos'


class CaptureAvd:
    def __init__(self, room_name, emulator_index):
        self.record = 0
        self.emulator_index = str(emulator_index)
        self.process = None
        dir_path = os.path.dirname(os.path.realpath(__file__))
        self.record_path = os.path.join(dir_path, IMG_DIR)
        self.detector = MotionDetection(room_name)
        self.index = 0

    def start(self):
        self.record = 1
        self.process = Process(target=self.record_process)
        self.process.start()

    def record_process(self):
        while True:
            # recording
            img_path = os.path.join(self.record_path, 'rec-{idx}.png'.format(idx=self.index))
            ret = os.system('{adb} -s emulator-{em} shell screencap -p /sdcard/rec-{idx}.png'
                            .format(adb=ADB_PATH, em=self.emulator_index, idx=self.index))
            if ret != 0:
                print('Process exited with non-zero return value: {sig}'.format(sig=ret))
                break
            ret = os.system('{adb} -s emulator-{em} pull /sdcard/rec-{idx}.png {img_path}'
                            .format(adb=ADB_PATH, em=self.emulator_index, idx=self.index, img_path=img_path))
            if ret != 0:
                print('Process exited with non-zero return value: {sig}'.format(sig=ret))
                break
            ret = os.system('{adb} -s emulator-{em} shell rm /sdcard/rec-{idx}.png'
                            .format(adb=ADB_PATH, em=self.emulator_index, idx=self.index))
            if ret != 0:
                print('Process exited with non-zero return value: {sig}'.format(sig=ret))
                break
            self.detector.add_image(img_path)
            self.index += 1
            time.sleep(0.5)
        pass
