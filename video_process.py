import cv2
import mediapipe as mp
from tqdm import tqdm
import time

#导入solution
mp_pose = mp.solutions.pose
#导入绘图函数
mp_drawing = mp.solutions.drawing_utils
#导入模型
pose = mp_pose.Pose(
    static_image_mode=False,
    model_complexity=2,
    smooth_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5)

#处理单帧的函数
def process_frame(img):
    start_time = time.time()
    h,w = img.shape[0],img.shape[1]
    img_RGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    results = pose.process(img_RGB)

    if results.pose_landmarks:
        mp_drawing.draw_landmarks(img,results.pose_landmarks,mp_pose.POSE_CONNECTIONS)

        for i in range(33):
            cx = int(results.pose_landmarks.landmark[i].x * w)
            cy = int(results.pose_landmarks.landmark[i].y * w)
            cz = results.pose_landmarks.landmark[i].z

            radius = 10
        #使用CV2的画圆点函数标出关键点，因为上面画过线了，关掉以免影响观感
        #     if i ==0:
        #         img = cv2.circle(img,(cx,cy),radius,(0,0,255),-1)
        #     elif i in [11,12]:
        #         img = cv2.circle(img,(cx,cy),radius,(223,155,6),-1)
        #     elif i in [23,24]:
        #         img = cv2.circle(img,(cx,cy),radius,(1,240,255),-1)
        #     elif i in [13,14]:
        #         img = cv2.circle(img,(cx,cy),radius,(140,47,240),-1)
        #     elif i in [25,26]:
        #         img = cv2.circle(img,(cx,cy),radius,(0,0,255),-1)
        #     elif i in [15,16,27,28]:
        #         img = cv2.circle(img,(cx,cy),radius,(223,155,60),-1)
        #     elif i in [17,19,21]:
        #         img = cv2.circle(img,(cx,cy),radius,(94,218,121),-1)
        #     elif i in [18,20,22]:
        #         img = cv2.circle(img,(cx,cy),radius,(16,144,247),-1)
        #     elif i in [27,29,31]:
        #         img = cv2.circle(img,(cx,cy),radius,(29,123,243),-1)
        #     elif i in [28,30,32]:
        #         img = cv2.circle(img,(cx,cy),radius,(193,182,255),-1)
        #     elif i in [9,10]:
        #         img = cv2.circle(img,(cx,cy),radius,(205,235,255),-1)
        #     elif i in [1,2,3,4,5,6,7,8]:
        #         img = cv2.circle(img,(cx,cy),radius,(94,218,121),-1)
        #     else:
        #         img = cv2.circle(img,(cx,cy),radius,(0,255,0),-1)
        # look_img(img)
    else:
        scaler = 1
        failure_str = "No person"
        img = cv2.putText(img,failure_str,(25 * scaler,100 * scaler),cv2.FONT_HERSHEY_SIMPLEX,0.75,(0,0,255),2)
    end_time = time.time()
    FPS = 1/(end_time - start_time)

    scaler = 1

    img = cv2.putText(img,"FPS"+str(int(FPS)),(25 * scaler,100 * scaler),cv2.FONT_HERSHEY_SIMPLEX,0.75,(0,0,255),2)
    return img

def generate_video(input_path="./4.mp4"):
    filehead = input_path.split("/")[-1]
    output_path = "out-" + filehead

    print("视频开始处理",input_path)

    cap = cv2.VideoCapture(input_path)
    frame_count = 0
    while(cap.isOpened()):
        sucess,frame = cap.read()
        frame_count += 1
        if not sucess:
            break
    cap.release()
    print("视频总帧数为",frame_count)

    cap = cv2.VideoCapture(input_path)
    frame_size = (cap.get(cv2.CAP_PROP_FRAME_WIDTH),cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    fourcc = cv2.VideoWriter_fourcc('M','P','4','V')
    fps = cap.get(cv2.CAP_PROP_FPS)

    out = cv2.VideoWriter(output_path,fourcc,fps,(int(frame_size[0]),int(frame_size[1])))

    with tqdm(total= frame_count-1) as pbar:
        try:
            while(cap.isOpened()):
                sucess,frame = cap.read()
                if not sucess:
                    break

                try:
                    frame = process_frame(frame)
                except:
                    print('')
                    pass
                if sucess == True:
                    out.write(frame)

                    pbar.update(1)

        except:
            print('中途中断')
            pass
    cv2.destroyAllWindows()
    out.release()
    cap.release()
    print('视频已保存',output_path)

generate_video(input_path="./4.mp4")