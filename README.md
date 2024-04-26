# Aruco_Marker

<img src= "https://github.com/AUTO-KKYU/Aruco_Marker/assets/118419026/4daac1c5-b667-459f-8704-dcd9fadb8b09" width="400" height="300">

- 마커는 좌표 체계가 있어 컴퓨터가 물체의 위치와 3차원 상의 자세(pose)를 파악 가능
- 3차원 자세 추정 방법 : 코너 좌표와 카메라 캘리브레이션을 통해 카메라 좌표계에서 3차원 자세를 추정

- Aruco marker로 할 수 있는 모든 과정을 진행하였다
- 캘리브레이션 과정을 통해 카메라와 aruco marker 사이의 거리 측정, 상대좌표, 방향 등등

## Clone this repo into the src directory 
```ruby
$ mkdir -p aruco_marker/src/
$ cd aruco_marker/src/
$ git clone https://github.com/AUTO-KKYU/Aruco_Marker.git
```
- OpenCV-Python version sensitivity is crucial
```ruby
$ pip uninstall opencv-contrib-python opencv-python
$ pip install opencv-contrib-python==4.7.0.68 opencv-python==4.7.0.68
```

## Getting Start  
**1) Generate AR**
- Please check and execute the files at your workspace location
- If you want to save the Aruco file in any folder of your choice, try modifying the code yourself
- Show 20 different kinds of ArUco markers when the 'q' button is pushed or exit the screen
```sh
$ python3 generate_aruco.py
```
<img src= "https://github.com/AUTO-KKYU/Aruco_Marker/assets/118419026/9a3037af-fff8-4cc8-88e1-0482035a62fb">

**2) Detect AR**
- Detect ArUco markers in real-time from a webcam feed and display their IDs
- The detected markers should have the same shape as the ones generated in step 1 (e.g., aruco.DICT_5X5_250)
- draw the contours of the detected markers
- Assign IDs to each ArUco marker for display on the screen
- The expected result is as follows
```sh
$ python3 detect_aruco.py
```
<img src= "https://github.com/AUTO-KKYU/Aruco_Marker/assets/118419026/8148d470-d46e-4ed5-8786-21fe37b89fbb)">

**3) Camera Calibration**
- Real-time detection of checkerboard patterns from webcam video -> Press 's' key to save the detected pattern as an image / Press 'q' key to exit the program
```sh
$ python3 capture_image.py
```
<img src= "https://github.com/AUTO-KKYU/Aruco_Marker/assets/118419026/9f33bf04-9eaa-447e-90c3-fd8b69594326">

- Detect a chess/checkerboard pattern from images and saves camera calibration data
```sh
$ python3 calibration_scripy.py
```
- check calibration data
```sh
$ python3 read_demo.py
```
<img src= "https://github.com/AUTO-KKYU/Aruco_Marker/assets/118419026/29fffb2a-9336-4e65-a2c7-9a09024c4f0c">

**4) Check Distance from camera**
- Detect ArUco markers in real-time from a webcam feed and display the position and distance of each marker
    - Detect ArUco markers
    - Calculate the position and distance of each marker
    - Detect x and y coordinates from the camera's center (Camera coordinate system)
<img src= "https://github.com/AUTO-KKYU/Aruco_Marker/assets/118419026/32c05c0e-3fba-4721-b35e-3c1d32a9c779">

**5) Detect ArUco markers in the front face**
- Code is not provided
- If you'd like to receive the code, please click on 'stars' and provide your email. I'll send it to you via GitHub Issue.

https://github.com/AUTO-KKYU/Aruco_Marker/assets/118419026/86d2d26a-9403-4fc3-adbe-e383faef313b

## Aruco Marker with ROS2
<img src= "https://github.com/AUTO-KKYU/Aruco_Marker/assets/118419026/48d55067-e407-4849-859e-ee3ede4cfa4c">

https://github.com/AUTO-KKYU/Aruco_Marker/assets/118419026/a435d5ce-7c57-42f6-aec4-5ca23147caaa
