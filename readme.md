# Digital Visual Effects Project #1

## Members

- B04902064 李衡
- B04902085 何鎧至

## Alignment

圖片對齊使用的是 median threshold bitmaps 的演算法，我們原先試過用 C++ 來寫，主因是能夠在時間和空間上有更好的控制程式的複雜度，我們用自己寫了一個 bitmap 專用的 class，讓每個 pixel 在實際上只使用一個 bit。[link here](https://github.com/henlium/medianThresholdBitmaps)

基於除錯的難度以及和其他部分銜接的方便性，我們轉用了 Python，算法參照原 paper 的作法，程式架構也與論文裡的大致類似，轉灰階的公式也參照了論文所提的作法。

## HDR

HDR 的部分我們用的是 Robertson 那篇的做法，因為這個算法需要算非常久(至少 8~10 次)才會開始 coverage，而遇到大圖的時候它跑一次就會需要很長的時間(大概一個小時)，如果要對三個 channel 都跑到 coverage 會花上數天。所以我們把原本拍的照片長跟寬都先縮小到 1/4，讓他對這張較小的圖片找出它的 G function(response function 的反函數)，再用這個 function 跑原本大圖來算出原圖的 Radius Map。G Function 的折線圖如下
![curveAll](mdimg/curveall.png)![curveLeft](mdimg/curveleft.png)![curveRight](mdimg/curveright.png)
可以發現在左右兩端的值是快速下降/上升的

## Tonemapping

這個部分我們使用的是外部程式來跑 Tone Mapping，結果如下

## Program

### How to use

- <code>python3 main.py -h</code> for help
- <code>-a</code> for alignment, <code>-g</code> to import known G function
- <code>-o</code> to specify output file's name, default is hdrimage.hdr
- when it use without <code>-g</code>, it will output G function to curve0.txt, curve1.txt, curve2.txt
- ex: <code>python3 main.py -a 2 -g img/01</code> to use alignment with known G function, and images are in <code>img/01</code>
- images filename must be <code>a:b.jpg</code> to represent exposure time is a/b

### Require modules

- opencv from image IO
- numpy for math calculation
- argparse for arguments

## Reference

1. [Mark Robertson, Sean Borman, Robert Stevenson, Estimation-Theoretic Approach to Dynamic Range Enhancement using Multiple Exposures, Journal of Electronic Imaging 2003.][1]
2. [Greg Ward, Fast, Robust Image Registration for Compositing High Dynamic Range Photographs from Hand-Held Exposures][2]

[1]:https://doi.org/10.1117/1.1557695
[2]:https://doi.org/10.1080/10867651.2003.10487583