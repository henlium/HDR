#!/usr/bin/env python3
import cv2 as cv
import numpy as np
from os import listdir
from Robertson import Robertson
import argparse
import align
import sys

def readFolder(folderName):
    fileNames = listdir(folderName)
    times = np.array([], dtype=np.float32)
    images = []
    for filename in fileNames:
        timestr = filename.split('.')
        if(timestr[1] != "JPG" and timestr[1] != "jpg"):
            continue
        timestr = timestr[0].split(':')
        time = float(int(timestr[0]))/float(int(timestr[1]))
        times = np.append(times, time)
        im = cv.imread(folderName + "/" +filename)
        images.append(im)
    # print(images)
    print(times)
    return images, times

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('folder',
                        help="Folder for pictures, filenames should represent exposure times in 1:100(1/100) format",
                        type=str, default='./img/05')
    parser.add_argument('-g', '--curve', 
                        help='if you have g function(inverse of reponse function), use this to run Robert HDR with it',
                        action="store_true")
    parser.add_argument('-a', '--align', 
                        help='Do alignment or not',
                        type=int, dest='level', default=-1)
    parser.add_argument('-c0', '--curve0', 
                        help='gfunction file for channel 0, only will be used when -g',
                        type=str, default='curve0.txt')
    parser.add_argument('-c1', '--curve1', 
                        help='gfunction file for channel 1, only will be used when -g',
                        type=str, default='curve1.txt')
    parser.add_argument('-c2', '--curve2', 
                        help='gfunction file for channel 2, only will be used when -g',
                        type=str, default='curve2.txt')
    parser.add_argument('-o', '--output',
                        help='output file name, default: hdrimage.hdr',
                        type=str, default='hdrimage.hdr')

    args = parser.parse_args()
    images, ExposureTimes = readFolder(args.folder)
    if(args.level >= 0):
        align.process(images, args.level)
    myhdr = Robertson()
    if(args.curve):
        curveFiles = [args.curve0, args.curve1, args.curve2]
        myhdrPic = myhdr.processwithcurve(images, ExposureTimes, curveFiles)
    else:
        myhdrPic = myhdr.process(images, ExposureTimes)
    cv.imwrite(args.output, myhdrPic)
