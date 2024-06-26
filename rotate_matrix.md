## 카메라 좌표계에서 월드 좌표계로 변환 (Camera Coordinates to World Coordinates)

카메라 캘리브레이션은 카메라가 캡처하는 이미지에서 객체의 3D 위치를 추정하기 위해 필수적이다. 이 과정에서 회전 행렬과 변환 행렬을 사용하여 카메라 좌표계에서 월드 좌표계로 좌표를 변환할 수 있음

1) 회전 행렬 생성: 오일러 각(Roll, Pitch, Yaw)을 사용하여 회전 행렬을 생성. 이 때, 회전은 일반적으로 Roll → Pitch  →Yaw 순서로 적용
2) 뷰 변환 행렬(VTM): 카메라가 바라보는 방향을 기준으로 좌표계를 재구성하기 위해 회전 행렬의 역행렬을 사용. 카메라가 바라볼 목표물을 설정하고, 카메라의 위치에서 목표물을 향하는 벡터를 생성한 후, 이 벡터를 기준으로 외적 연산을 활용하여 뷰 변환 행렬을 만든다
3) 회전 행렬 검증: 입력된 3x3 회전 행렬 R이 유효한 회전 행렬인지 확인
4) 오일러 앵글 변환: 유효한 회전 행렬을 오일러 앵글로 변환

<img src= "https://github.com/AUTO-KKYU/Aruco_Marker/assets/118419026/07eb2a80-156a-4060-9e91-503bf045db01">

https://github.com/AUTO-KKYU/Aruco_Marker/assets/118419026/cab69687-0418-4ca8-8ed6-62c10eb3a979
