import cv2 as cv
import numpy as np 
from stack import stackImages
import time


red_yellow_lower = [0, 104, 49]
red_yellow_upper = [35, 255, 255]

blue_lower = [54, 100, 51]
blue_upper = [137, 255, 255]

def empty(a):
    pass

def get_shapes(img, img_contour, color):

    img_blur = cv.GaussianBlur(img, (3,3), 1)
    img_gray = cv.cvtColor(img_blur, cv.COLOR_BGR2GRAY)

    med_val = np.median(img_gray) 
    lower = int(max(0 ,0.7*med_val))
    upper = int(min(255,1.3*med_val))
    img_canny = cv.Canny(image=img, threshold1=lower,threshold2=upper)

    # img_canny = cv.Canny(img_gray, 200, 225)
    kernel = np.ones((5,5))
    img = cv.dilate(img_canny, kernel, iterations=1)
    contours, hierarchy = cv.findContours(img, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)

    for contour in contours:
        area = cv.contourArea(contour)

        min_area = 1000
        if area > min_area:
            #cv.drawContours(img_contour, contour, -1, (255, 0, 255), 7)
            perimeter = cv.arcLength(contour, True)
            approx = cv.approxPolyDP(contour, 0.042*perimeter, True)

            x, y, w, h = cv.boundingRect(approx)
            # cv.putText(img_contour, "Points: " + str(len(approx)), (x, y-20), cv.FONT_HERSHEY_COMPLEX, 0.7, (0,0,255), 2)
            # cv.putText(img_contour, "Area: " + str(area), (x, y-40), cv.FONT_HERSHEY_COMPLEX, 0.7, (0,0,255), 2)
            # cv.putText(img_contour, "Color: " + color, (x, y-60), cv.FONT_HERSHEY_COMPLEX, 0.7, (0,0,255), 2)
            cv.rectangle(img_contour, (x,y), (x+w, y+h), (0,255,0), 5)
            
            
            if 8 >= len(approx) >= 6 and color=="blue":
                cv.putText(img_contour, "Znak Nakazu", (x, y), cv.FONT_HERSHEY_COMPLEX, 0.7, (0,0,255), 2)

            elif len(approx) == 4 and color == "blue":
                cv.putText(img_contour, "Znak Informacyjny", (x, y), cv.FONT_HERSHEY_COMPLEX, 0.7, (0,0,255), 2)

            elif 8 >= len(approx) >= 6 and color=="red":
                cv.putText(img_contour, "Znak Zakazu", (x, y), cv.FONT_HERSHEY_COMPLEX, 0.7, (0,0,255), 2)

            elif len(approx) == 3 and color=="red":
                cv.putText(img_contour, "Znak Ostrzegawczy", (x, y), cv.FONT_HERSHEY_COMPLEX, 0.7, (0,0,255), 2)

            elif len(approx) == 4 and color=="red":
                cv.putText(img_contour, "Znak Informacyjny", (x, y), cv.FONT_HERSHEY_COMPLEX, 0.7, (0,0,255), 2)
            
            else:
                cv.putText(img_contour, "Nierozpoznany", (x, y), cv.FONT_HERSHEY_COMPLEX, 0.7, (0,0,255), 2)
def color_space(img, lower, upper):
    hsv_frame = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    img_contour = frame.copy()

    lower = np.array(lower, dtype=np.uint8) 
    upper = np.array(upper, dtype=np.uint8) 
    mask = cv.inRange(hsv_frame, lower, upper)

    kernel = np.ones((7,7), "uint8")
    mask = cv.morphologyEx(mask, cv.MORPH_CLOSE, kernel)

    res = cv.bitwise_and(frame, frame, mask=mask)

    return res


if __name__ == "__main__":

    frame_width, frame_height = 500, 500
    capture = cv.VideoCapture(0)
    capture.set(3, frame_width)
    capture.set(4, frame_height)

    # cv.namedWindow('Parameters')
    # cv.resizeWindow('Parameters', 840, 840)
    # cv.createTrackbar('RM_LB', 'Parameters', 0, 255, empty)
    # cv.createTrackbar('RM_LG', 'Parameters', 104, 255, empty)
    # cv.createTrackbar('RM_LR', 'Parameters', 49, 255, empty)
    # cv.createTrackbar('RM_UB', 'Parameters', 35, 255, empty)
    # cv.createTrackbar('RM_UG', 'Parameters', 255, 255, empty)
    # cv.createTrackbar('RM_UR', 'Parameters', 255, 255, empty)

    # cv.createTrackbar('BM_LB', 'Parameters', 54, 255, empty)
    # cv.createTrackbar('BM_LG', 'Parameters', 100, 255, empty)
    # cv.createTrackbar('BM_LR', 'Parameters', 51, 255, empty)
    # cv.createTrackbar('BM_UB', 'Parameters', 137, 255, empty)
    # cv.createTrackbar('BM_UG', 'Parameters', 255, 255, empty)
    # cv.createTrackbar('BM_UR', 'Parameters', 255, 255, empty)

    while(1):
        _, frame = capture.read()
        img_contour = frame.copy()

        img = color_space(frame, red_yellow_lower, red_yellow_upper)
        get_shapes(img, img_contour, "red")

        img = color_space(frame, blue_lower, blue_upper)
        get_shapes(img, img_contour, "blue")

        img_stack = stackImages(0.8, ([frame, img, img_contour]))
        cv.imshow("Result", img_stack)

        if cv.waitKey(1)  & 0xFF == ord('q'):
            break

