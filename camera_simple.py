import cv2
import mediapipe as mp
from tqdm import tqdm
import time

#导入solution和绘图函数
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

#导入模型
pose = mp_pose.Pose(
    static_image_mode= False,
    model_complexity=2,
    smooth_landmarks=True,
    enable_segmentation=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5)

#处理帧函数
def process_frame(img):
    img_RGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = pose.process(img_RGB)
    # 可视化
    mp_drawing.draw_landmarks(img, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
    # look_img(img)
    # mp_drawing.plot_landmarks(results.pose_world_landmarks, mp_pose.POSE_CONNECTIONS)

    # img_RGB = cv2.cvtCOLOR(img, cv2.COLOR_BGR2RGB)
    # results = hands.process(img_RGB)

    # if results.multi_hand_landmarks:
    #    for hand_idx in range(len(results.multi_hand_landmarks)):
    #        hand_21 = results.multi_hand_landmarks[hand_idx]
    #        mpDraw.draw_landmarks(img, hand_21, mp_hands.HAND_CONNECTIONS)
    return img




#调用摄像头获取每一帧
cap = cv2.VideoCapture(0)
cap.open(0)
while cap.isOpened():
    success, frame = cap.read()
    if not success:
        print('Error')
        break

    frame = process_frame(frame)
    cv2.imshow('camera_simple',frame)

    if cv2.waitKey(1) in [ord('q'),27]:
        break
cap.release
cv2.destroyAllWindows