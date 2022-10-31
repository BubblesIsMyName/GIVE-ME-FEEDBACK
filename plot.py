import pandas as pd
import numpy as np
import util
import csv


def export_pose(results,df_path):
    
    # Export coordinates
    try:
        # Extract Pose landmarks
        hands_results = results.multi_hand_landmarks # Normalised landmarks - distances [0,1]
        hands_row = np.array([[item.x, 1-item.y, item.z] for item in hands_results[0].landmark]).flatten().tolist()
        
        # Export to CSV
        with open(df_path, mode='a', newline='') as f:
            csv_writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            csv_writer.writerow(hands_row) 
        
    except Exception as e:
        pass

from cv2 import ROTATE_90_COUNTERCLOCKWISE
import cv2 # Import opencv
import mediapipe as mp # Import mediapipe
# Import the pose capture methods from mediapipe
mp_drawing = mp.solutions.drawing_utils # Drawing helpers
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

settings_dict = util.read_settings()

# For Prediciton
import pickle
with open(settings_dict["model"], 'rb') as f:
    model_rf = pickle.load(f)

columns = ['x0','y0','z0','x1','y1','z1','x2','y2','z2','x3','y3','z3','x4','y4','z4','x5','y5','z5','x6','y6','z6','x7','y7','z7','x8','y8','z8','x9','y9','z9','x10','y10','z10','x11','y11','z11','x12','y12','z12','x13','y13','z13','x14','y14','z14','x15','y15','z15','x16','y16','z16','x17','y17','z17','x18','y18','z18','x19','y19','z19','x20','y20','z20']
df = pd.DataFrame(columns=columns)

def predict_gesture(data):
    gesture = ["other"] # The default initial gesture set
    try:
        hands_results = data.multi_hand_landmarks # Normalised landmarks - distances [0,1]
        hands_row = np.array([[item.x, 1-item.y, item.z] for item in hands_results[0].landmark]).flatten().tolist()
        df.loc[0]= hands_row
        gesture = model_rf.predict(df)
    except:
        pass
    return gesture
    

def capture_from_web_cam(capture,gesture_count):
    """
    Captures the data from the web camera
    
    """
    print("in capture from web cam")

    gesture_prev = "other"
    # df_path = settings_dict["df"] # For capturing data for training.
    count = 0
    gesture_dict = {
        "peace":0,
        "rock_on":1,
        "thumb_up":2,
        "other":3
    }
    while True:
        if capture.value:
            try:
                cap = cv2.VideoCapture(settings_dict["video_ip"]) # Capturing from the web camera
                # Initiate holistic model
                with mp_hands.Hands(model_complexity=0,
                                    min_detection_confidence=0.5,
                                    min_tracking_confidence=0.5,
                                    max_num_hands=1) as hands:
                    while cap.isOpened():
                            count +=1
                            
                            success, frame = cap.read()
                            if not success:
                                print("Camera frame empty")
                                continue # if webcam stream

                            # Recolor Feed
                            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                            image.flags.writeable = False        
                            image = cv2.rotate(image,rotateCode=ROTATE_90_COUNTERCLOCKWISE)
                            # Make Detections
                            results = hands.process(image)
                            gesture = predict_gesture(results)[0]
                            if gesture != gesture_prev:
                                print(capture.value)
                                print(f"{gesture}:{count}")
                                to_update = gesture_dict[gesture]
                                gesture_count[to_update] = gesture_count[to_update]+1
                                print(gesture_count[to_update])
                            gesture_prev = gesture

                            # For capturing data for training 
                            # export_pose(results,df_path)
                            
                            
                            # Recolor image back to BGR for rendering
                            image.flags.writeable = True   
                            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                            
                            if results.multi_hand_landmarks:
                                for hand_landmarks in results.multi_hand_landmarks:
                                    mp_drawing.draw_landmarks(
                                        image,
                                        hand_landmarks,
                                        mp_hands.HAND_CONNECTIONS,
                                        mp_drawing_styles.get_default_hand_landmarks_style(),
                                        mp_drawing_styles.get_default_hand_connections_style())
                                            
                            cv2.imshow('Raw Webcam Feed', image)
                            # Stop playing
                            if (cv2.waitKey(1) & 0xFF == ord('q')) or not capture.value:
                                break

                cap.release()
                cv2.destroyAllWindows()
            except Exception as e:
                print(e)

