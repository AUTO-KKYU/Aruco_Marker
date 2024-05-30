import numpy as np
import argparse
from utils import ARUCO_DICT
import cv2
import sys
import os

# 입력 파라미터 설정
ap = argparse.ArgumentParser()
ap.add_argument("-o", "--output", required=True, help="path to output folder to save ArUCo tag")
ap.add_argument("-i", "--id", type=int, required=True, help="ID of ArUCo tag to generate")
ap.add_argument("-t", "--type", type=str, default="DICT_ARUCO_ORIGINAL", help="type of ArUCo tag to generate")
ap.add_argument("-s", "--size", type=int, default=200, help="Size of the ArUCo tag")
args = vars(ap.parse_args())

# Check to see if the dictionary is supported
if ARUCO_DICT.get(args["type"], None) is None:
	print(f"ArUCo tag type '{args['type']}' is not supported")
	sys.exit(0)

arucoDict = cv2.aruco.Dictionary_get(ARUCO_DICT[args["type"]])
print("Generating ArUCo tag of type '{}' with ID '{}'".format(args["type"], args["id"]))

tag_size = args["size"]
tag = np.zeros((tag_size, tag_size, 1), dtype="uint8")
cv2.aruco.drawMarker(arucoDict, args["id"], tag_size, tag, 1)

# 저장할 폴더 경로 생성
cur_dir = os.getcwd()
save_dir = cur_dir + '/' + args["output"] + '/'

# 저장할 폴더가 없다면, 해당 폴더 생성
try:
	os.makedirs(save_dir)

except OSError: 
       if not os.path.isdir(save_dir): 
           raise

# aruco 마커 이미지 저장
tag_name = f'{args["type"]}_id_{args["id"]}.png'
cv2.imwrite(save_dir + tag_name, tag)