import numpy as np
from utils import ARUCO_DICT, aruco_display
import argparse
import cv2
import sys
import os

# 입력 파라미터 설정
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="path to input image containing ArUCo tag")
ap.add_argument("-t", "--type", type=str, default="DICT_ARUCO_ORIGINAL", help="type of ArUCo tag to detect")
ap.add_argument("-o", "--output", required=True, help="path to output folder to save ArUCo tag")
args = vars(ap.parse_args())

# ArUCo 마커 이미지 읽기
print("Loading image...")
cur_dir = os.getcwd()
image = cv2.imread(cur_dir + '/' + args["image"])

# 이미지 전처리
h,w,_ = image.shape
width=600
height = int(width*(h/w))
image = cv2.resize(image, (width, height), interpolation=cv2.INTER_CUBIC)

# verify that the supplied ArUCo tag exists and is supported by OpenCV
if ARUCO_DICT.get(args["type"], None) is None:
	print(f"ArUCo tag type '{args['type']}' is not supported")
	sys.exit(0)

# load the ArUCo dictionary, grab the ArUCo parameters, and detect
# the markers
print("Detecting '{}' tags....".format(args["type"]))
arucoDict = cv2.aruco.Dictionary_get(ARUCO_DICT[args["type"]])
arucoParams = cv2.aruco.DetectorParameters_create()
corners, ids, rejected = cv2.aruco.detectMarkers(image, arucoDict, parameters=arucoParams)

print(f"corners : {corners}")
print(f"ids : {ids}")

# ArUCo 마커 검출 결과에 대한 시각화
detected_markers = aruco_display(corners, ids, rejected, image)

# 저장할 폴더 경로 생성
save_dir = cur_dir + '/' + args["output"] + '/'

# 저장할 폴더가 없다면, 해당 폴더 생성
try:
	os.makedirs(save_dir)

except OSError: 
       if not os.path.isdir(save_dir): 
           raise

# aruco 마커 이미지 저장
img_name_split = args["image"].split('/')
tag_name = f'{img_name_split[-1]}_detect_result.png'
cv2.imwrite(save_dir + tag_name, detected_markers)