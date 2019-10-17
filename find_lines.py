"""
How to run:
python find_lines.py <image path>
"""
from __future__ import print_function

import argparse
import cv2
import os

from guiutils import LineFinder


def main():
    parser = argparse.ArgumentParser(description='Visualizes the line for hough transform.')
    parser.add_argument('filename')

    args = parser.parse_args()

    img = cv2.imread(args.filename, cv2.IMREAD_GRAYSCALE)

    if img.shape[0] > img.shape[1]:
        img = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)

    # cv2.namedWindow('input', cv2.WINDOW_NORMAL)
    # cv2.resizeWindow('input', 1378, 598)
    # cv2.imshow('input', img)

    edge_finder = LineFinder(img, filter_size=13, threshold1=28, threshold2=115)

    print("Edge parameters:")
    print("GaussianBlur Filter Size: %f" % edge_finder.filterSize())
    print("Threshold1: %f" % edge_finder.threshold1())
    print("Threshold2: %f" % edge_finder.threshold2())

    (head, tail) = os.path.split(args.filename)

    (root, ext) = os.path.splitext(tail)

    smoothed_filename = os.path.join("output_images", root + "-smoothed" + ext)
    edge_filename = os.path.join("output_images", root + "-edges" + ext)

    cv2.imwrite(smoothed_filename, edge_finder.smoothedImage())
    cv2.imwrite(edge_filename, edge_finder.edgeImage())

    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
