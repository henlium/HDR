#!/usr/bin/env python
# coding: utf-8

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np

def gray(img):
    return np.array([[(54*yi[0]+183*yi[1]+19*yi[2])/256 for yi in xi] for xi in img], dtype='uint8')

# Shrink an 1-channel image by 2
def shrinkBy2(img):
    retImg =         np.array([[(int(img[i][j])+int(img[i][j+1])+int(img[i+1][j])+int(img[i+1][j+1]))/4            for j in range(0, img.shape[1]-1, 2)]            for i in range(0, img.shape[0]-1, 2)] , dtype='uint8')
    return retImg

# Compute an 1-channel image's threshold bitmap and exclusion bitmap
# Return them in a tuple
def bitmap(img):
    med = int(np.median(img))
    thresBitmap = np.array([[True if yi > med else False for yi in xi] for xi in img], dtype='bool')
    x, y = img.shape
    excluBitmap = np.ones((x, y), dtype='bool')
    for i in range(x):
        for j in range(y):
            if abs(img[i][j] - med) < 5:
                excluBitmap[i][j] = False
    return (thresBitmap, excluBitmap)

def getExpShift(img0, img1, shiftBits):
    if shiftBits > 0:
        smlImg0 = shrinkBy2(img0)
        smlImg1 = shrinkBy2(img1)
        curShiftBits = getExpShift(smlImg0, smlImg1, shiftBits-1)
        print(curShiftBits)
        curShiftBits[0] *= 2
        curShiftBits[1] *= 2
    else:
        curShiftBits = (0, 0)
    tb0, eb0 = bitmap(img0)
    tb1, eb1 = bitmap(img1)
    minErr = img0.shape[0] * img0.shape[1]
    for i in range(-1, 2):
        for j in range(-1, 2):
            xs = curShiftBits[0] + i
            ys = curShiftBits[1] + j
            shifted_tb1 = np.full(tb1.shape, False, dtype='bool')
            shifted_eb1 = np.full(eb1.shape, False, dtype='bool')
            if xs > 0:
                shifted_tb1[xs:] = tb1[:-xs]
                shifted_eb1[xs:] = eb1[:-xs]
            elif xs < 0:
                shifted_tb1[:xs] = tb1[-xs:]
                shifted_eb1[:xs] = eb1[-xs:]
            else:
                shifted_tb1 = tb1
                shifted_eb1 = eb1
            if ys > 0:
                shifted_tb1 = [np.append([False] * ys, row[:-ys]) for row in shifted_tb1]
                shifted_eb1 = [np.append([False] * ys, row[:-ys]) for row in shifted_eb1]
            elif ys < 0:
                shifted_tb1 = [np.append(row[-ys:], [False] * -ys) for row in shifted_tb1]
                shifted_eb1 = [np.append(row[-ys:], [False] * -ys) for row in shifted_eb1]
            diff_b = np.logical_xor(tb0, shifted_tb1)
            diff_b = np.logical_and(eb0, diff_b)
            diff_b = np.logical_and(shifted_eb1, diff_b)
            err = np.sum(shifted_eb1)
            if err < minErr:
                ret = [xs, ys]
                minErr = err
            print(xs, ys, 'err', err)
    return ret

def align(img0_name, img1_name, level):
    img0 = mpimg.imread(img0_name)
    img1 = mpimg.imread(img1_name)
    g0 = gray(img0)
    g1 = gray(img1)
    return getExpShift(g0, g1, level)
