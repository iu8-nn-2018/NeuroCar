#!/usr/bin/env python

import cv2 as cv
import subprocess

def start():
        return cv.VideoCapture(0)

def end(capture):
        subprocess.call('rm image.jpg', shell=True)
        capture.release()
        cv.destroyAllWindows()

def read_picture(capture):
        frame = capture.read()
        cv.imwrite('image.jpg', frame[1])
        file = open("image.jpg", "rb")
        return file.read()

