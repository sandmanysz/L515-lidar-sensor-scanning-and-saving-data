The script "data_collection.py" is used to collect RGB image, depth image and point cloud.

Just need call "get_image_data" function and given the related RGB resolution and depth resolution.

RGB_resolution_dictionary={'0': [1920,1080], '1':[1280_720], '2':[640,480], '3':[640,360]}
depth_resolution_dictionary = {'0': [1024,768], '1':[640,480]} 

suggest use the largest resolution which means that RGB input is '0' and depth input is '0'.

The input Path is to provide the saving address.

The video will show when you call the function, then press the 'q' to saving data when you fill the data is good. The saving file will be labeled the saving time.

