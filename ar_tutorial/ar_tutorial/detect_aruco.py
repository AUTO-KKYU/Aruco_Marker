from rclpy.node import Node, ParameterDescriptor
import rclpy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
from cv2 import aruco
import numpy as np

class ArucoDetector(Node):
    def __init__(self):
        super().__init__('aruco_detector')

        self.declare_parameter('camera_topic', '/camera')
        self.declare_parameter('thrs1', 127)
        self.declare_parameter('calib_data_path', '/home/kkyu/project_study/src/ar_tutorial/ar_tutorial/ros_aruco/4. calib_data/MultiMatrix.npz', 
            ParameterDescriptor(dynamic_typing=True))
        self.declare_parameter('marker_dict_type', 'DICT_5X5_250', 
            ParameterDescriptor(dynamic_typing=True))
        self.declare_parameter('marker_size', 6, 
            ParameterDescriptor(dynamic_typing=True))
        self.declare_parameter('camera_height', 1.0, 
            ParameterDescriptor(dynamic_typing=True))

        self.camera_topic = self.get_parameter('camera_topic').value
        self.thrs1 = self.get_parameter('thrs1').value

        self.bridge = CvBridge()
        self.subscription = self.create_subscription(
            Image,
            self.camera_topic,
            self.callback_img,
            10
        )
        self.publisher = self.create_publisher(Image, '/front_aruco', 10)

        calib_data_path = self.get_parameter('calib_data_path').value
        dict_type = self.get_parameter('marker_dict_type').value
        self.MARKER_SIZE = self.get_parameter('marker_size').value
        self.CAMERA_HEIGHT = self.get_parameter('camera_height').value

        calib_data = np.load(calib_data_path)
        self.cam_mat = calib_data['camMatrix']
        self.dist_coef = calib_data['distCoef']
        self.rVec = calib_data["rVector"]
        self.tVec = calib_data["tVector"]

        self.marker_dict = aruco.getPredefinedDictionary(getattr(aruco, dict_type))
        self.param_markers = aruco.DetectorParameters()

    def callback_img(self, msg):
        cv_img = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        gray_frame = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)
        distance_text= ''

        marker_corners, marker_IDs, _ = aruco.detectMarkers(gray_frame, self.marker_dict, parameters=self.param_markers)

        if marker_corners:
            self.rVec, self.tVec, _ = aruco.estimatePoseSingleMarkers(
                marker_corners, self.MARKER_SIZE, self.cam_mat, self.dist_coef
            )
            total_markers = range(0, marker_IDs.size)
            for ids, corners, i in zip(marker_IDs, marker_corners, total_markers):
                cv2.polylines(
                    cv_img, [corners.astype(np.int32)], True, (0, 255, 255), 4, cv2.LINE_AA
                )
                corners = corners.reshape(4, 2)
                corners = corners.astype(int)
                top_right = corners[0].ravel()
                top_left = corners[1].ravel()
                bottom_right = corners[2].ravel()
                bottom_left = corners[3].ravel()
                distance = np.sqrt(
                    self.tVec[i][0][2] ** 2 + self.tVec[i][0][0] ** 2 + self.tVec[i][0][1] ** 2
                )
                horizontal_distance = self.tVec[i][0][0]

                horizontal_distance_meters = horizontal_distance * self.CAMERA_HEIGHT / self.tVec[i][0][2]

                point = cv2.drawFrameAxes(cv_img, self.cam_mat, self.dist_coef, self.rVec[i], self.tVec[i], 4, 4)
                cv2.putText(
                    cv_img,
                    f"id: {ids[0]} Dist: {round(distance, 2)}",
                    top_right,
                    cv2.FONT_HERSHEY_PLAIN,
                    1,
                    (0, 0, 255),
                    2,
                    cv2.LINE_AA,
                )
                cv2.putText(
                    cv_img,
                    f"x:{round(self.tVec[i][0][0],1)} y: {round(self.tVec[i][0][1],1)} ",
                    bottom_right,
                    cv2.FONT_HERSHEY_PLAIN,
                    0.8,
                    (0, 0, 255),
                    2,
                    cv2.LINE_AA,
                )

                if abs(self.tVec[i][0][0]) <= 1 and abs(self.tVec[i][0][1]) <= 1:
                    direction_text = "Front"
                    direction_color = (0, 255, 0)  # Green
                    curve_text = "Curve: 0 degree"
                else:
                    curve_degree = np.arctan(horizontal_distance / self.tVec[i][0][1]) * (180 / np.pi)
                    curve_text = f"Curve: {abs(curve_degree):.1f} degree"
                    if self.tVec[i][0][0] > 0:
                        direction_text = "Right"
                        distance_text = f"{abs(horizontal_distance_meters):.3f} right of center"
                    else:
                        direction_text = "Left"
                        distance_text = f"{abs(horizontal_distance_meters):.3f} left of center"
                    direction_color = (255, 255, 255)  # White

                # Display direction text
                cv2.putText(
                    cv_img,
                    f"Direction: {direction_text}",
                    (20, 50),
                    cv2.FONT_HERSHEY_PLAIN,
                    1.5,
                    direction_color,
                    2,
                    cv2.LINE_AA,
                )
                cv2.putText(
                    cv_img,
                    curve_text,
                    (20, 100),
                    cv2.FONT_HERSHEY_PLAIN,
                    1.5,
                    (255, 255, 255),  # White
                    2,
                    cv2.LINE_AA,
                )
                cv2.putText(
                    cv_img,
                    f"{distance_text}",
                    (20, 150),
                    cv2.FONT_HERSHEY_PLAIN,
                    1.5,
                    (255, 255, 255),  # White
                    2,
                    cv2.LINE_AA,
                )

        pub_aruco = self.bridge.cv2_to_imgmsg(cv_img, 'bgr8')
        self.publisher.publish(pub_aruco)

def main(args=None):
    rclpy.init(args=args)
    node = ArucoDetector()
    rclpy.spin(node)
    node.destroy_node
