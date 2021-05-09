import pyrealsense2 as rs
import numpy as np
import cv2
import time

def get_image_data(RGB_resolution,depth_resolution,Path):
    # RGB_resolution_dictionary={'1920_1080': [1920,1080], '1280_720':[1280_720], '640_480':[640,480], '640_360':[640,360]}
    # depth_resolution_dictionary = {'1024_768': [1024,768], '1024_480': [1024,480],'640_480':[640,480]}
    RGB_resolution_dictionary={'0': [1920,1080], '1':[1280,720], '2':[640,480], '3':[640,360]}
    depth_resolution_dictionary = {'0': [1024,768], '1': [640,480]}
    pc = rs.pointcloud()
    # points = rs.points()
    # Configure depth and color streams
    pipeline = rs.pipeline()
    config = rs.config()
    config.enable_stream(rs.stream.depth, depth_resolution_dictionary[str(depth_resolution)][0], depth_resolution_dictionary[str(depth_resolution)][1], rs.format.z16, 30)
    config.enable_stream(rs.stream.color, RGB_resolution_dictionary[str(RGB_resolution)][0], RGB_resolution_dictionary[str(RGB_resolution)][1], rs.format.bgr8, 30)
    # preset_range = depth_sensor.get_option_range(rs.option.visual_preset)
    # Start streaming
    cfg = pipeline.start(config)
    dev = cfg.get_device()
    depth_sensor = dev.first_depth_sensor()
    depth_sensor.set_option(rs.option.visual_preset, 3)
    while True:
        align_to = rs.stream.color
        align = rs.align(align_to)

        # image collection and we start collect it from 11th frame to avoid distortion.
        for i in range(10):
            data = pipeline.wait_for_frames()
            # depth = data.get_depth_frame() # original depth data
            # color = data.get_color_frame() # original color data
        aligned_frames = align.process(data)
        depth=aligned_frames.get_depth_frame()
        color=aligned_frames.get_color_frame()




        # get extrin and intrinsic parameter
        dprofile = depth.get_profile()
        cprofile = color.get_profile()

        cvsprofile = rs.video_stream_profile(cprofile)
        dvsprofile = rs.video_stream_profile(dprofile)
        color_intrin = cvsprofile.get_intrinsics()
        print(color_intrin)
        depth_intrin = dvsprofile.get_intrinsics()
        print(depth_intrin)
        extrin = dprofile.get_extrinsics_to(cprofile)
        print(extrin)

        depth_image = np.asanyarray(depth.get_data())
        color_image = np.asanyarray(color.get_data())

        pc.map_to(color)


        colorful = np.asanyarray(color.get_data())
        colorful=colorful.reshape(-1,3)

        # get the vertex coordinate
        points = pc.calculate(depth)
        vtx = np.asanyarray(points.get_vertices())

        # Apply colormap on depth image (image must be converted to 8-bit per pixel first)
        depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.1), cv2.COLORMAP_JET)
        cv2.namedWindow('RGB', cv2.WINDOW_AUTOSIZE)
        cv2.namedWindow('depth',cv2.WINDOW_AUTOSIZE)
        cv2.imshow('RGB',color_image)
        cv2.imshow('depth',depth_colormap)

        key=cv2.waitKey(1)
        # key 'q' to stop the images showing and save the image and point cloud.
        if key & 0xFF == ord('q') or key == 27:
            cv2.destroyAllWindows()
            now=int(round(time.time()*1000))
            now_time=time.strftime('%Y-%m-%d_%H_%M_%S_',time.localtime(now/1000))
            print('saving images ...')
            cv2.imwrite(Path+now_time+'_'+'color_image.jpg', color_image)
            cv2.imwrite(Path+now_time+'_'+'depth_image.jpg', depth_image)
            cv2.imwrite(Path+now_time+'_'+'depth_colorMAP.jpg', depth_colormap)

            print('saving pcl....')
            # comment by siyuan because of try other method for saving point cloud
            with open(now_time+'_'+'point_cloud.txt', 'w') as f:
                for i in range(len(vtx)):
                    f.write(str(np.float(vtx[i][0])) + ' ' + str(np.float(vtx[i][1])) + ' ' + str(
                        np.float(vtx[i][2])) + '\n')
            print('save done')
            break








if __name__ == '__main__':
    # RGB_resolution_dictionary={'0': [1920,1080], '1':[1280_720], '2':[640,480], '3':[640,360]}
    # depth_resolution_dictionary = {'0': [1024,768], '1':[640,480]}
    RGB_resolution=0
    depth_resolution=0
    path='C:/Users/siyua/PycharmProjects/fiber_mold_datacollection/dataset/' # data_saving_address
    get_image_data(RGB_resolution=RGB_resolution,depth_resolution=depth_resolution,Path=path)
    # Key 'q' to stop the monitoring and save whole data.