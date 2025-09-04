import cv2
import numpy as np
import math
import matplotlib.pyplot as plt

def cal_two(x_hough):
    src = cv2.imread("Male/221020_103912_0000000031_CAM1_OK.bmp", cv2.IMREAD_COLOR)
    if src is None: raise Exception("영상 파일 읽기 오류")
    src=cv2.resize(src,(1216, 1020))


    gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    corner = cv2.cornerHarris(gray, 2, 3, 0.04)
    coord = np.where(corner > 0.1* corner.max())#변화량 결과의 최대값 10% 이상의 좌표 구하기
    coord = np.stack((coord[1], coord[0]), axis=1)


    circle_arr=[]
    for x, y in coord:

        cv2.circle(src, (x,y), 5, (0,0,255), 1, cv2.LINE_AA)
        circle_arr.append([x,y])

    circle_arr.sort()

    tmp=0

    for i in range(len(circle_arr),0,-1):
        x_circle = circle_arr[i-1][0]
        print(x_circle)

        if (tmp-x_circle)>110:
            x2=x_circle
            print(x2)
            cv2.circle(src, (circle_arr[i-1][0], circle_arr[i-1][1]), 8, (255, 0, 255), 1, cv2.LINE_AA)
            break
        tmp=x_circle
    plt.imshow(src)
    plt.show()
    mid=x2-50-circle_arr[0][0]

    length_1=mid/x_hough
    print("x2=",mid)
    print("circle_arr=",circle_arr[0][0])
    print("x_hough=",x_hough)
    print(length_1)

    return length_1

def cal_hough():
    src = cv2.imread("Scale14.69.bmp", cv2.IMREAD_COLOR)
    if src is None: raise Exception("영상 파일 읽기 오류")

    src=cv2.resize(src,(1216, 1020))


    canny = cv2.Canny(src,1,2,apertureSize = 3)

    lines = cv2.HoughLines(canny, 0.8, np.pi / 180, 150, srn=100, stn=200, min_theta=0, max_theta=np.pi)

    line_arr = []
    for i in lines:
        rho, theta = i[0][0], i[0][1]
        a, b = np.cos(theta), np.sin(theta)
        x0, y0 = a * rho, b * rho

        scale = src.shape[0] + src.shape[1]

        x1 = int(x0 + scale * -b)
        y1 = int(y0 + scale * a)
        x2 = int(x0 - scale * -b)
        y2 = int(y0 - scale * a)

        rad = math.atan2(y2 - y1, x2 - x1)
        PI = math.pi
        deg = (rad * 180) / PI

        if abs(deg) > 75 and abs(deg) <= 100:

            cv2.line(src, (x1, y1), (x2, y2), (0, 0, 255), 2)
            line_arr.append([x1, y1, x2, y2])

    line_arr.sort()

    x_m = line_arr[2][0]-line_arr[1][0]#자에서 한 눈금만큼의 픽셀값

    print("x_m=",x_m)
    return x_m


x_hough=cal_hough()
print("길이 2는 {:.2f}cm".format(cal_two(x_hough)))