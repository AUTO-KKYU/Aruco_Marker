import numpy as np 

loaded_arrays = np.load("C:\\Users\\dknjy\\.anaconda\\ros_aruco\\4. calib_data\\MultiMatrix.npz")
print(loaded_arrays.files)
print(loaded_arrays["camMatrix"])