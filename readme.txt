Requirement environment:
Python3, Opencv, numpy, pyrealsense2.


The script "data_collection.py" is used to collect RGB image, depth image and point cloud.

Just need call "get_image_data" function and give the related RGB resolution, depth resolution and data saving address.

Below is resolution selection from RGB and depth.
RGB_resolution_dictionary={'0': [1920,1080], '1':[1280_720], '2':[640,480], '3':[640,360]}
depth_resolution_dictionary = {'0': [1024,768], '1':[640,480]} 

Suggest to use the largest resolution which means that RGB input is '0' and depth input is '0'.

The real time video will show when you call the function, then press the 'q' to stop video and save data when you feel the data is good. The saving file will be named by the saving time.

