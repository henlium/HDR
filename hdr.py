#!/usr/bin/env python3
import cv2 as cv
import numpy as np
from Robertson import Robertson
def readImagesAndTimes():
    times = np.array([12.884, 9.935, 4, 3.221, 1, 15782/19599, 0.25, 0.2, 1/60, 1/80, 1/315, 1/405, 1/1002], dtype=np.float32)
    filenames = "img/exposures/img"
    images = []
    for i in range(1, 14):
        if(i < 10):
            im = cv.imread(filenames + '0' + str(i) + ".jpg")
        else:
            im = cv.imread(filenames + str(i) + ".jpg")
        images.append(im)
    return images, times


images, ExposureTimes = readImagesAndTimes()
# X = images[0].shape[0];
# Y = images[0].shape[1];
merge_robertson = cv.createMergeRobertson()
hdr_robertson = merge_robertson.process(images, times=ExposureTimes.copy())
cv.imwrite("hdrRobertson.hdr", hdr_robertson)

myhdr = Robertson()
myhdrPic = myhdr.process(images, ExposureTimes)
cv.imwrite("myhdr.hdr", myhdrPic)

