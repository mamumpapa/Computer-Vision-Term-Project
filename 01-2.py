import cv2
import numpy as np
import math

def cal_hough():
    src = cv2.imread("Scale14.69.bmp", cv2.IMREAD_COLOR)
    if src is None: raise Exception("영상 파일 읽기 오류")

    src=cv2.resize(src,(1216, 1020))


    gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)

    canny = cv2.Canny(src,1,2,apertureSize = 3)

    cv2.imshow("canny",canny)
    cv2.waitKey(0)
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
            x_arr = np.array([x1, x2])
            y_arr = np.array([y1, y2])
            arr = np.clip(x_arr, 0, 1440)
            arr2 = np.clip(y_arr, 0, 1080)

            cut_x = int((arr[0] + arr[1]) / 2)
            cut_y = arr2[0]
            cut_x2 = int((arr[0] + arr[1]) / 2)
            cut_y2 = arr2[1]

            cv2.line(src, (x1, y1), (x2, y2), (0, 0, 255), 2)
            line_arr.append([x1, y1, x2, y2])

    line_arr.sort()

    x_m = line_arr[1][0]-line_arr[0][0]

    print(x_m)
    return x_m