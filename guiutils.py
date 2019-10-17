from __future__ import print_function
from builtins import object
import cv2, sys, math
import numpy as np


class EdgeFinder(object):
    def __init__(self, image, filter_size=1, threshold1=0, threshold2=0):
        self.image = image
        self._filter_size = filter_size
        self._threshold1 = threshold1
        self._threshold2 = threshold2

        def onchangeThreshold1(pos):
            self._threshold1 = pos
            self._render()

        def onchangeThreshold2(pos):
            self._threshold2 = pos
            self._render()

        def onchangeFilterSize(pos):
            self._filter_size = pos
            self._filter_size += (self._filter_size + 1) % 2
            self._render()

        cv2.namedWindow('edges', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('edges', 1378, 598)

        # cv2.namedWindow('smoothed', cv2.WINDOW_NORMAL)
        # cv2.resizeWindow('smoothed', 1378, 598)

        cv2.createTrackbar('threshold1', 'edges', self._threshold1, 255, onchangeThreshold1)
        cv2.createTrackbar('threshold2', 'edges', self._threshold2, 255, onchangeThreshold2)
        cv2.createTrackbar('filter_size', 'edges', self._filter_size, 20, onchangeFilterSize)

        self._render()

        print("Adjust the parameters as desired.  Hit any key to close.")

        cv2.waitKey(0)

        cv2.destroyWindow('edges')
        cv2.destroyWindow('smoothed')

    def threshold1(self):
        return self._threshold1

    def threshold2(self):
        return self._threshold2

    def filterSize(self):
        return self._filter_size

    def edgeImage(self):
        return self._edge_img

    def smoothedImage(self):
        return self._smoothed_img

    def _render(self):
        self._smoothed_img = cv2.GaussianBlur(self.image, (self._filter_size, self._filter_size), sigmaX=0, sigmaY=0)
        self._edge_img = cv2.Canny(self._smoothed_img, self._threshold1, self._threshold2)
        #cv2.imshow('smoothed', self._smoothed_img)
        cv2.imshow('edges', self._edge_img)



class LineFinder(object):
    def __init__(self, image, filter_size=1, threshold1=0, threshold2=0):
        self.image = image
        self._filter_size = filter_size
        self._threshold1 = threshold1
        self._threshold2 = threshold2

        def onchangeThreshold1(pos):
            self._threshold1 = pos
            self._render()

        def onchangeThreshold2(pos):
            self._threshold2 = pos
            self._render()

        def onchangeFilterSize(pos):
            self._filter_size = pos
            self._filter_size += (self._filter_size + 1) % 2
            self._render()

        cv2.namedWindow('edges', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('edges', 1378, 598)
        cv2.namedWindow('lines', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('lines', 1378, 598)
        cv2.namedWindow('linesP', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('linesP', 1378, 598)
        cv2.createTrackbar('threshold1', 'edges', self._threshold1, 255, onchangeThreshold1)
        cv2.createTrackbar('threshold2', 'edges', self._threshold2, 255, onchangeThreshold2)
        cv2.createTrackbar('filter_size', 'edges', self._filter_size, 20, onchangeFilterSize)
        self._render()
        print("Adjust the parameters as desired.  Hit any key to close.")
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def threshold1(self):
        return self._threshold1

    def threshold2(self):
        return self._threshold2

    def filterSize(self):
        return self._filter_size

    def edgeImage(self):
        return self._edge_img

    def smoothedImage(self):
        return self._smoothed_img

    def _render(self):
        self._smoothed_img = cv2.GaussianBlur(self.image, (self._filter_size, self._filter_size), sigmaX=0, sigmaY=0)
        self._edge_img = cv2.Canny(self._smoothed_img, self._threshold1, self._threshold2)
        cv2.imshow('edges', self._edge_img)

        self._cdst = cv2.cvtColor(self._edge_img, cv2.COLOR_GRAY2BGR)
        lines = cv2.HoughLines(self._edge_img, 1, np.pi / 180, 150, None, 0, 0)
        if lines is not None:
            for i in range(0, len(lines)):
                rho = lines[i][0][0]
                theta = lines[i][0][1]
                a = math.cos(theta)
                b = math.sin(theta)
                x0 = a * rho
                y0 = b * rho
                pt1 = (int(x0 + 1000*(-b)), int(y0 + 1000*(a)))
                pt2 = (int(x0 - 1000*(-b)), int(y0 - 1000*(a)))
                cv2.line(self._cdst, pt1, pt2, (0,0,255), 3, cv2.LINE_AA)
        cv2.imshow('lines', self._cdst)

        self._cdstP = np.copy(self._cdst)
        linesP = cv2.HoughLinesP(self._edge_img, 1, np.pi / 180, 50, None, 50, 10)
        if linesP is not None:
            for i in range(0, len(linesP)):
                l = linesP[i][0]
                cv2.line(self._cdstP, (l[0], l[1]), (l[2], l[3]), (0,0,255), 3, cv2.LINE_AA)
        cv2.imshow('linesP', self._cdst)
