from __future__ import division

import time
import os
import subprocess
import datetime

import picamera
import picamera.array
import numpy as np

class MyMotionDetector(picamera.array.PiMotionAnalysis):
    def __init__(self, camera, handler):
        super(MyMotionDetector, self).__init__(camera)
        self.handler = handler
        self.first = True
        self.a15 = [0]*20
        self.a30 = [0]*20
        self.a60 = [0]*20
        self.c = 0

    def analyse(self, a):
        a = np.sqrt(
            np.square(a['x'].astype(np.float)) +
            np.square(a['y'].astype(np.float))
        ).clip(0, 255).astype(np.uint8)
        self.a15[self.c]= (15 < a ).sum()
        self.a30[self.c]= (30 < a ).sum()
        self.a60[self.c]= (60 < a ).sum()
        self.c = (self.c+1)%20
        sum15 = 0
        sum30 = 0
        sum60 = 0
        for i in range(20):
            sum15+=self.a15[i]
            sum30+=self.a30[i]
            sum60+=self.a60[i]
        result = [int(sum15/20),int(sum30/20),int(sum60/20)]
        self.handler.motion_detected(result)

class CaptureHandler:
    def __init__(self, camera, post_capture_callback=None):
        self.camera = camera
        self.callback = post_capture_callback
        self.detected = False
        self.working = False
        self.i = 0

    def motion_detected(self,val):
    	print val

class PiMotion:
    def __init__(self, verbose=False, post_capture_callback=None):
        self.verbose = verbose
        self.post_capture_callback = post_capture_callback

    def __print(self, str):
        if self.verbose:
            print str

    def start(self):
        with picamera.PiCamera() as camera:
            camera.resolution = (1280, 720)
            camera.framerate = 8

            handler = CaptureHandler(camera, self.post_capture_callback)

            self.__print('Waiting 2 seconds for the camera to warm up')
            time.sleep(2)

            try:
                self.__print('Started recording')
                camera.start_recording(
                    '/dev/null', format='h264',
                    motion_output=MyMotionDetector(camera, handler)
                )

                while True:
                    time.sleep(1)
            finally:
                camera.stop_recording()
                self.__print('Stopped recording')

def callback(path):
	print 'Callback'


def signal_handler(signal, frame):
    print 'You pressed Ctrl-C!'
    sys.exit(0)

motion = PiMotion(verbose=True, post_capture_callback=callback)
motion.start()