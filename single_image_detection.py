import cv2
import mediapipe as mp
import matplotlib.pyplot as plt
#%matplotlib inline

#定义可视化图像函数
def look_img(img):
    img_RGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    plt.imshow(img_RGB)
    plt.show()

#导入模型
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
#mp_pose.Pose? 直接运行获取帮助文档

pose = mp_pose.Pose(static_image_mode=True, #静态图片还是连续视频帧
                    model_complexity=2, #人体姿态关键点检测模型，0 lite,1 full,2 heavy,除1外，需手动导入
                    smooth_landmarks=True,  #平滑关键点
                    enable_segmentation=True,   #人体抠图
                    min_detection_confidence=0.5,   #置信度阈值
                    min_tracking_confidence=0.5)    #追踪阈值

#读入图像，显示原图
img = cv2.imread('haitu.jpg')
look_img(img)

#图像输入模型获取结果
img_RGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
results = pose.process(img_RGB) #BGR转RGB

#可视化结果
mp_drawing.draw_landmarks(img, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
look_img(img)   #带线条的图像
# 用于生成纯线条图，在三维真实物理坐标系可视化以米作为单位的检测结果
mp_drawing.plot_landmarks(results.pose_world_landmarks, mp_pose.POSE_CONNECTIONS)

