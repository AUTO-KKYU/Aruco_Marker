import cv2 as cv
import numpy as np
import math
from cv2 import aruco

def isRotationMatrix(R):
    Rt = np.transpose(R)
    shouldBeIdentity = np.dot(Rt, R)
    I = np.identity(3, dtype=R.dtype)
    n = np.linalg.norm(I - shouldBeIdentity)
    return n < 1e-6  # Consider precision errors

def rotationMatrixToEulerAngles(R):
    if not isRotationMatrix(R):
        print("Warning: Matrix is not a valid rotation matrix.")
        return np.array([0, 0, 0])  # Return a default or handle this case as needed
    
    sy = math.sqrt(R[0, 0] ** 2 + R[1, 0] ** 2)
    singular = sy < 1e-6
    if not singular:
        x = math.atan2(R[2, 1], R[2, 2])
        y = math.atan2(-R[2, 0], sy)
        z = math.atan2(R[1, 0], R[0, 0])
    else:
        x = math.atan2(-R[1, 2], R[1, 1])
        y = math.atan2(-R[2, 0], sy)
        z = 0
    return np.array([x, y, z])

# Load calibration data
calib_data_path = "/home/kkyu/test/ros_aruco/4. calib_data/MultiMatrix.npz"
calib_data = np.load(calib_data_path)
cam_mat = calib_data["camMatrix"]
dist_coef = calib_data["distCoef"]

# Define constants and dictionary
MARKER_SIZE = 6  # Size of the marker in centimeters
marker_dict = aruco.getPredefinedDictionary(aruco.DICT_5X5_250)
param_markers = aruco.DetectorParameters()

# Start video capture
cap = cv.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break
    gray_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    marker_corners, marker_IDs, _ = aruco.detectMarkers(gray_frame, marker_dict, parameters=param_markers)

    if marker_corners:
        rVec, tVec, _ = aruco.estimatePoseSingleMarkers(marker_corners, MARKER_SIZE, cam_mat, dist_coef)
        for i in range(marker_IDs.size):
            rMat = cv.Rodrigues(rVec[i])[0]
            euler_angles = rotationMatrixToEulerAngles(rMat)
            yaw = euler_angles[1]  # Yaw is the second element, rotation around y-axis

            realworld_tvec = tVec[i][0]
            tvec_str = "x=%4.0f y=%4.0f yaw=%4.0f" % (realworld_tvec[0], realworld_tvec[1], math.degrees(yaw))
            cv.putText(frame, tvec_str, (20, 460), cv.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2, cv.LINE_AA)

            # Draw the pose of the marker
            cv.drawFrameAxes(frame, cam_mat, dist_coef, rVec[i], tVec[i], 4, 4)

    cv.imshow("frame", frame)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv.destroyAllWindows()
