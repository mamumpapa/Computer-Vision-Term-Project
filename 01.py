import cv2
import numpy as np
import math
import matplotlib.pyplot as plt

def cal_one(x_hough):
    src = cv2.imread("Male/221020_103912_0000000031_CAM1_OK.bmp", cv2.IMREAD_COLOR)
    if src is None: raise Exception("영상 파일 읽기 오류")
    src=cv2.resize(src,(1216, 1020))


    gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)

    corner = cv2.cornerHarris(gray, 2, 3, 0.04)
    coord = np.where(corner > 0.1* corner.max())
    coord = np.stack((coord[1], coord[0]), axis=-1)

    circle_arr=[]
    for x, y in coord:
        cv2.circle(src, (x,y), 5, (0,0,255), 1, cv2.LINE_AA)
        circle_arr.append([x,y])

    circle_arr.sort()

    x_circle = circle_arr[-1][0]-circle_arr[0][0]
    print(x_circle)
    length_1=x_circle/x_hough
    print(length_1)

    plt.imshow(src)
    plt.show()

    return length_1

def cal_hough():
    src = cv2.imread("Scale14.69.bmp", cv2.IMREAD_COLOR)
    if src is None: raise Exception("영상 파일 읽기 오류")

    src=cv2.resize(src,(1216, 1020))


    canny = cv2.Canny(src,1,2,apertureSize = 3)

    lines = cv2.HoughLines(canny, 0.8, np.pi / 180, 150, srn=100, stn=200, min_theta=0, max_theta=np.pi)

    line_arr = []
    for i in lines:
        rho, theta = i[0][0], i[0][1]#처음 직선이 그려지는 x 위치 값과 theta 값

        a, b = np.cos(theta), np.sin(theta)#theta의 cos, sin 값
        x0, y0 = a * rho, b * rho#x 위치 값에 cos(theta)와 sin(theta)를 곱함
        scale = src.shape[0]#이미지의 y값

        x1 = int(x0 + scale * -b)#검출된 직선의 맨 밑 좌표와 맨 위 좌표
        y1 = int(y0 + scale * a)
        x2 = int(x0 - scale * -b)
        y2 = int(y0 - scale * a)

        rad = math.atan2(y2 - y1, x2 - x1)#라디안을 계산
        PI = math.pi
        deg = (rad * 180) / PI#180을 곱하고 파이로 나누어 각도를 계산
        if abs(deg) > 89 and abs(deg) <= 91:
            print(rho)
            print(x0,y0)
            cv2.line(src, (x1, y1), (x2, y2), (0, 0, 255), 2)
            line_arr.append([x1, y1, x2, y2])
            #각도가 약 90도 일 경우 검출된 선을 그리고 리스트에 삽입

    line_arr.sort()#리스트를 정렬시킴

    x_m = line_arr[2][0]-line_arr[1][0]#리스트 중 앞에서 3번째 직선과 2번째 직선을 계산(값이 가장 정확함)

    plt.imshow(src)
    plt.show()
    print("x_m=",x_m)
    return x_m


x_hough=cal_hough()
print("길이 1은 {:.2f}cm".format(cal_one(x_hough)))