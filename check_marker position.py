import cv2
import numpy as np
import time

if __name__ == "__main__":
    cap = cv2.VideoCapture("/dev/video0")
    
    camera_matrix = np.array([
        [3.4196423e+03, 0.0000000e+00, 3.1801168e+02],
        [0.0000000e+00, 3.4430821e+03, 2.3948030e+02],
        [0.0000000e+00, 0.0000000e+00, 1.0000000e+00]
    ])

    dist_coeffs = np.array([
        -4.98287773e+00, -3.79634367e+02,  5.19871306e-02, -4.70900630e-02, -1.83785065e+00
    ])
    
    # aruco detector 생성
    board_type = cv2.aruco.DICT_4X4_50
    aruco_dict = cv2.aruco.getPredefinedDictionary(board_type)
    parameters = cv2.aruco.DetectorParameters()
    detector = cv2.aruco.ArucoDetector(aruco_dict, parameters)
    
    time.sleep(2)
    
    # 파란색상 정의
    blue_BGR = (255, 0, 0)

    # 마커사이즈 실제 사이즈와 공간 좌표(x,y,z) -> z가 0인 이유는 마커가 평면이기 때문이다.
    marker_size = 400
    marker_3d_edges = np.array([
        [0, 0, 0],
        [0, marker_size, 0],
        [marker_size, marker_size, 0],
        [marker_size, 0, 0]
    ], dtype='float32').reshape((4, 1, 3))

    while True:
        ret, img = cap.read()
        if not ret:
            print("Failed to capture image")
            break
        
        # 마커(marker) 검출
        corners, ids, rejectedCandidates = detector.detectMarkers(img)

        # 검출된 마커들의 꼭지점을 이미지에 그려 확인
        if corners:
            for corner in corners:
                corner = np.array(corner).reshape((4, 2))
                (topLeft, topRight, bottomRight, bottomLeft) = corner

                topRightPoint = (int(topRight[0]), int(topRight[1]))
                topLeftPoint = (int(topLeft[0]), int(topLeft[1]))
                bottomRightPoint = (int(bottomRight[0]), int(bottomRight[1]))
                bottomLeftPoint = (int(bottomLeft[0]), int(bottomLeft[1]))

                cv2.circle(img, topLeftPoint, 4, blue_BGR, -1)
                cv2.circle(img, topRightPoint, 4, blue_BGR, -1)
                cv2.circle(img, bottomRightPoint, 4, blue_BGR, -1)
                cv2.circle(img, bottomLeftPoint, 4, blue_BGR, -1)
                
                # PnP
                ret, rvec, tvec = cv2.solvePnP(marker_3d_edges, corner, camera_matrix, dist_coeffs)
                if ret:
                    x = round(tvec[0][0], 2)
                    y = round(tvec[1][0], 2)
                    z = round(tvec[2][0], 2)
                    rx = round(np.rad2deg(rvec[0][0]), 2)
                    ry = round(np.rad2deg(rvec[1][0]), 2)
                    rz = round(np.rad2deg(rvec[2][0]), 2)
                    # PnP 결과를 이미지에 그려 확인
                    text1 = f"{x},{y},{z}"
                    text2 = f"{rx},{ry},{rz}"
                    cv2.putText(img, text1, (int(topLeft[0]-10), int(topLeft[1]+10)), cv2.FONT_HERSHEY_PLAIN, 1.0, (0, 0, 255))
                    cv2.putText(img, text2, (int(topLeft[0]-10), int(topLeft[1]+40)), cv2.FONT_HERSHEY_PLAIN, 1.0, (0, 0, 255))
        
        cv2.imshow("img", img)
        key = cv2.waitKey(1)
        if key == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()
