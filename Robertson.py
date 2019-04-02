import numpy as np
import math

class EmUnit():
    def __init__(self, Number, X, Y):
        self.X = X
        self.Y = Y
        self.Number = Number

class Robertson():
    def __init__(self):
        self.MAXITERATOR = 15
        self.THRESHOLD = 0.1
        self.curve = np.zeros([3, 256], dtype='float32')

        self.weight = np.zeros(256, dtype='float32')
        q = 255 / 4.0
        e4 = math.exp(4.0)
        scale = e4/(e4 - 1.0)
        shift = 1.0 / (1.0 - e4)
        for i in range(256):
            value = i / q - 2.0
            value = scale * math.exp(-value * value) + shift
            self.weight[i] = value

    def processwithcurve(self, images, ExposureTimes, filenames):
        height, width, null = images[0].shape
        for filename in filenames:
            filename = "curve" + str(i) + ".txt"
            curve[i] = np.loadtxt(filename)

        HDRPic = np.zeros([height, width, 3], dtype='float32')
        HDRPic[:, :, 0] = self.calcRadius(images, ExposureTimes, self.curve[0], 0)
        HDRPic[:, :, 1] = self.calcRadius(images, ExposureTimes, self.curve[1], 1)
        HDRPic[:, :, 2] = self.calcRadius(images, ExposureTimes, self.curve[2], 2)
        return HDRPic
    
    def process(self, images, ExposureTimes):
        height, width, null = images[0].shape
        for i in range(3):
            self.curve[i, :] = self.findCurve(i, images, ExposureTimes)
            filename = "curve" + str(i) + ".txt"
            np.savetxt(filename, self.curve[i])

        HDRPic = np.zeros([height, width, 3], dtype='float32')
        HDRPic[:, :, 0] = self.calcRadius(images, ExposureTimes, self.curve[0], 0)
        HDRPic[:, :, 1] = self.calcRadius(images, ExposureTimes, self.curve[1], 1)
        HDRPic[:, :, 2] = self.calcRadius(images, ExposureTimes, self.curve[2], 2)
        return HDRPic

    def calcRadius(self, images, ExposureTimes, gFunc, channel):
        height, width, null = images[0].shape
        Ei = np.zeros([height, width], dtype='float32')
        for i in range(height):
            for j in range(width):
                u, b = 0.0, 0.0 
                for n in range(len(images)):
                    z = images[n][i, j, channel]
                    u += self.weight[z] * gFunc[z] * ExposureTimes[n]
                    b += self.weight[z] * ExposureTimes[n] * ExposureTimes[n]
                Ei[i,j] = u/b
        return Ei
        
    def findCurve(self, channel, images, ExposureTimes):
        height, width, null = images[0].shape
        Em = {}
        for i in range(256):
            Em[i] = []
        for n in range(len(images)):
            for i in range(height):
                for j in range(width): 
                    m = images[n][i, j, channel] 
                    Em[m].append(EmUnit(n, i, j))

        #assume response function is linear
        gFunc = np.zeros(256, dtype='float32')
        for i in range(256):
            gFunc[i] = ((float)(i) / 128.0)#init as linear
        
        #calc radius map with assumed response function
        Ei = self.calcRadius(images, ExposureTimes, gFunc, channel)

        calcTimes = 0
        lastSum = 0
        while calcTimes <= self.MAXITERATOR:
            print(str(calcTimes) + "/" + str(self.MAXITERATOR) + " times")
            #calc response function by radius map
            gFunc = np.zeros(256, dtype='float32') 
            for i in range(256):
                for j in range(0,len(Em[i])):
                    gFunc[i] += Ei[Em[i][j].X, Em[i][j].Y] * ExposureTimes[Em[i][j].Number]
                if len(Em[i]) > 0:
                    gFunc[i] /= len(Em[i])
            gFunc /= gFunc[128] #normalize

            #evaluate radius map by new response time
            Ei = self.calcRadius(images, ExposureTimes, gFunc, channel)
            
            #minimize
            totalSum = 0.0
            for n in range(len(images)):
                for i in range(height):
                    for j in range(width):
                        totalSum += self.weight[images[n][i, j, channel]] * (gFunc[images[n][i, j, channel]] - Ei[i,j] * ExposureTimes[n])
            print("lastSum: " + str(lastSum) + ", totalSum: " + str(totalSum))
            if calcTimes == 0:
                lastSum = totalSum
            else:
                if abs(lastSum - totalSum) < self.THRESHOLD:
                    print("End due to converge," + str(calcTimes) + " times.")
                    return gFunc
            lastSum = totalSum
            calcTimes += 1

        print("End due to run more than " + str(self.MAXITERATOR) + " times.")
        return gFunc
