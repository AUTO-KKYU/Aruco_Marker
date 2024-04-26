import cv2 as cv
from cv2 import aruco
import numpy as np

# load in the calibration data
calib_data_path = "/home/kkyu/Downloads/ros_aruco-20240422T093125Z-001/ros_aruco/4. calib_data/MultiMatrix.npz"

calib_data = np.load(calib_data_path)
print(calib_data.files)

cam_mat = calib_data["camMatrix"]
dist_coef = calib_data["distCoef"]
r_vectors = calib_data["rVector"]
t_vectors = calib_data["tVector"]

MARKER_SIZE = 6  # centimeters (measure your printed marker size)
CAMERA_HEIGHT = 1.0  # Assume camera height from the ground is 1.0 meter

marker_dict = aruco.getPredefinedDictionary(aruco.DICT_5X5_250)

param_markers = aruco.DetectorParameters()

cap = cv.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break
    gray_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    marker_corners, marker_IDs, reject = aruco.detectMarkers(
        gray_frame, marker_dict, parameters=param_markers
    )
    if marker_corners:
        rVec, tVec, _ = aruco.estimatePoseSingleMarkers(
            marker_corners, MARKER_SIZE, cam_mat, dist_coef
        )
        total_markers = range(0, marker_IDs.size)
        for ids, corners, i in zip(marker_IDs, marker_corners, total_markers):
            cv.polylines(
                frame, [corners.astype(np.int32)], True, (0, 255, 255), 4, cv.LINE_AA
            )
            corners = corners.reshape(4, 2)
            corners = corners.astype(int)
            top_right = corners[0].ravel()
            top_left = corners[1].ravel()
            bottom_right = corners[2].ravel()
            bottom_left = corners[3].ravel()

            # Calculating the distance
            distance = np.sqrt(
                tVec[i][0][2] ** 2 + tVec[i][0][0] ** 2 + tVec[i][0][1] ** 2
            )

            # Calculate horizontal distance from camera center
            horizontal_distance = tVec[i][0][0]

            # Convert horizontal distance to meters
            horizontal_distance_meters = horizontal_distance * CAMERA_HEIGHT / tVec[i][0][2]

            # Draw the pose of the marker
            point = cv.drawFrameAxes(frame, cam_mat, dist_coef, rVec[i], tVec[i], 4, 4)
            cv.putText(
                frame,
                f"id: {ids[0]} Dist: {round(distance, 2)}",
                top_right,
                cv.FONT_HERSHEY_PLAIN,
                1,
                (0, 0, 255),
                2,
                cv.LINE_AA,
            )
            cv.putText(
                frame,
                f"x:{round(tVec[i][0][0],1)} y: {round(tVec[i][0][1],1)} ",
                bottom_right,
                cv.FONT_HERSHEY_PLAIN,
                0.8,
                (0, 0, 255),
                2,
                cv.LINE_AA,
            )

            # Determine front, left, or right
            if abs(tVec[i][0][0]) <= 1 and abs(tVec[i][0][1]) <= 1:
                direction_text = "Front"
                direction_color = (0, 255, 0)  # Green
                curve_text = "Curve: 0 degree"
            else:
                curve_degree = np.arctan(horizontal_distance / tVec[i][0][1]) * (180 / np.pi)
                curve_text = f"Curve: {abs(curve_degree):.1f} degree"
                if tVec[i][0][0] > 0:
                    direction_text = "Right"
                    distance_text = f"{abs(horizontal_distance_meters):.3f} right of center"
                else:
                    direction_text = "Left"
                    distance_text = f"{abs(horizontal_distance_meters):.3f} left of center"
                direction_color = (255, 255, 255)  # White

            # Display direction text
            cv.putText(
                frame,
                f"Direction: {direction_text}",
                (20, 50),
                cv.FONT_HERSHEY_PLAIN,
                1.5,
                direction_color,
                2,
                cv.LINE_AA,
            )
            cv.putText(
                frame,
                curve_text,
                (20, 100),
                cv.FONT_HERSHEY_PLAIN,
                1.5,
                (255, 255, 255),  # White
                2,
                cv.LINE_AA,
            )
            cv.putText(
                frame,
                f"Distance from center: {distance_text}",
                (20, 150),
                cv.FONT_HERSHEY_PLAIN,
                1.5,
                (255, 255, 255),  # White
                2,
                cv.LINE_AA,
            )
    cv.imshow("frame", frame)
    key = cv.waitKey(1)
    if key == ord("q"):
        break
cap.release()
cv.destroyAllWindows()
