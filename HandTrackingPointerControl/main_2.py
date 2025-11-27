import cv2
import mediapipe as mp
import pyautogui
import math
import time
import threading
import subprocess

#Get screen size
screen_width, screen_height = pyautogui.size()

# Initialize Mediapipe Face Detection
mp_face = mp.solutions.face_mesh
face=mp_face.FaceMesh(min_detection_confidence=0.5, min_tracking_confidence=0.5)

# Initialize Mediapipe Hand Detection
mp_hand = mp.solutions.hands
hands = mp_hand.Hands(
   # static_image_mode=False,
   # max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# Initialize Camera
camera = cv2.VideoCapture(0)
camera.set(cv2.CAP_PROP_FRAME_WIDTH,640 )
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

last_time=0
#prev_x, prev_y = 0, 0

def thanos_snap():
    pyautogui.hotkey('command','q')
    print("snap")

def minimize():
    pyautogui.hotkey('command','m')

def hand_tips():
    index_finger = hand_landmarks.landmark[mp_hand.HandLandmark.INDEX_FINGER_TIP]
    thumb_finger = hand_landmarks.landmark[mp_hand.HandLandmark.THUMB_TIP]
    thumb_base = hand_landmarks.landmark[mp_hand.HandLandmark.THUMB_CMC]
    middle_finger = hand_landmarks.landmark[mp_hand.HandLandmark.MIDDLE_FINGER_TIP]
    pinky_finger = hand_landmarks.landmark[mp_hand.HandLandmark.PINKY_TIP]
    ring_finger = hand_landmarks.landmark[mp_hand.HandLandmark.RING_FINGER_TIP]

    return index_finger,thumb_finger,thumb_base,middle_finger,pinky_finger,ring_finger

def draw_landmarks(frame, hand_landmarks):
    landmark_drawing_spec = mp_draw.DrawingSpec(color=(0, 0, 255), thickness=2, circle_radius=1)
    connection_drawing_spec = mp_draw.DrawingSpec(color=(0, 255, 0), thickness=2)
    mp_draw.draw_landmarks(
        frame,
        hand_landmarks,
        mp_hand.HAND_CONNECTIONS,
        landmark_drawing_spec,
        connection_drawing_spec
    )

def move(index_finger, frame_width, frame_height):
    global prev_x, prev_y
    x_index = int(index_finger.x * frame_width)
    y_index = int(index_finger.y * frame_height)
    screen_x = int(x_index * screen_width / frame_width) * 2
    screen_y = int(y_index * screen_height / frame_height) * 2
    SMOOTHING = 0.6
    prev_x = prev_x * (1 - SMOOTHING) + screen_x * SMOOTHING
    prev_y = prev_y * (1 - SMOOTHING) + screen_y * SMOOTHING

    pyautogui.moveTo(int(prev_x), int(prev_y), duration=0.001)
    return y_index

def click(thumb_finger,thumb_base,frame_height,frame_width):
    distance_thumb = math.hypot(
        (thumb_finger.x - thumb_base.x) * frame_width,
        (thumb_finger.y - thumb_base.y) * frame_height
    )
    if distance_thumb < 87:
        pyautogui.click()


    cv2.putText(
        frame,
        f'H_Distance: {int(distance_thumb)}',
        (40, 50),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (255, 0, 0),
        2
    )
def double_click(index_finger,middle_finger,frame_height,frame_width):

    distance_middle_thumb = math.hypot(
        (index_finger.x - middle_finger.x) * frame_width,
        (index_finger.y - middle_finger.y) * frame_height
    )
    if distance_middle_thumb < 20:
        pyautogui.doubleClick()
        pyautogui.hotkey('command','o')
        time.sleep(0.5)
        print("double click")

def scroll(y_index,frame_height):
    if y_index < (frame_height // 2 - 100):
        pyautogui.scroll(2)
    elif y_index > (frame_height // 2):
        pyautogui.scroll(-2)

brightness_updating = False

def increase_brightness():
    global brightness_updating
    if brightness_updating:
        return
    brightness_updating = True
    for _ in range(2):
        subprocess.run(["osascript", "-e", 'tell application "System Events" to key code 144'])
        time.sleep(0.1)
    brightness_updating = False

def decrease_brightness():
    global brightness_updating
    if brightness_updating:
        return
    brightness_updating = True
    for _ in range(2):
        subprocess.run(["osascript", "-e", 'tell application "System Events" to key code 145'])  # Decrease brightness
        time.sleep(0.1)
    brightness_updating = False



def angry(face_landmarks, frame_width):
    left_inner_eyebrow = face_landmarks.landmark[70]  # Left inner eyebrow
    right_inner_eyebrow = face_landmarks.landmark[300]  # Right inner eyebrow
    eyebrow_distance = abs(left_inner_eyebrow.x - right_inner_eyebrow.x) * frame_width -4

    print(f"Eyebrow Distance: {eyebrow_distance}")

    angry_threshold = 91.5

    return eyebrow_distance < angry_threshold

def get_face_distance(face_landmarks):
    forehead = face_landmarks.landmark[10]  # Forehead landmark
    chin = face_landmarks.landmark[152]  # Chin landmark

    face_height = abs(forehead.y - chin.y) * frame_height

    cv2.putText(frame, f'F_Distance: {int(face_height)}', (380, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

def get_volume():
    result = subprocess.run(["osascript", "-e", "output volume of (get volume settings)"], capture_output=True, text=True)
    return int(result.stdout.strip())

# Function to increase volume
def increase_volume():
    subprocess.run(["osascript", "-e", "set volume output volume (output volume of (get volume settings) + 10)"])

# Function to decrease volume
def decrease_volume():
    subprocess.run(["osascript", "-e", "set volume output volume (output volume of (get volume settings) - 10)"])


def volume_bar(current_volume):
    bar_x, bar_y = 50, 70
    bar_height = 200
    max_volume = 100
    bar_fill = int((current_volume / max_volume) * bar_height)

    cv2.rectangle(frame, (bar_x, bar_y), (bar_x + 40, bar_y + bar_height), (255, 255, 255), 2)
    cv2.rectangle(frame, (bar_x, bar_y + (bar_height - bar_fill)), (bar_x + 40, bar_y + bar_height), (0, 255, 0),
                  -1)
    cv2.putText(frame, f"Volume: {current_volume}%", (bar_x, bar_y + bar_height + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6,
                (0, 255, 0), 2)



try:
    while True:
        ret, frame = camera.read()
        if not ret:
            print("Failed to grab frame.")
            break


        frame = cv2.flip(frame, 1)
        frame_height, frame_width, _ = frame.shape
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb_frame)
        prev_x, prev_y = 0, 0

        results_face = face.process(rgb_frame)
        current_volume = get_volume()
        if results_face.multi_face_landmarks and not results.multi_hand_landmarks:
            for face_landmarks in results_face.multi_face_landmarks:
                top_lip = face_landmarks.landmark[13]  # Upper lip center
                bottom_lip = face_landmarks.landmark[14]  # Lower lip center
                get_face_distance(face_landmarks)

                lip_distance = abs(top_lip.y - bottom_lip.y)
                if lip_distance > 0.01:
                    threading.Thread(target=increase_brightness, daemon=True).start()

                if angry(face_landmarks, frame_width):
                    threading.Thread(target=decrease_brightness, daemon=True).start()




        if results.multi_hand_landmarks:

            for hand_landmarks in results.multi_hand_landmarks:
                draw_landmarks(frame, hand_landmarks)
                index_finger,thumb_finger,thumb_base,middle_finger,pinky_finger,ring_finger=hand_tips()
                y_index=move(index_finger,frame_width,frame_height)
                click(thumb_finger,thumb_base,frame_height,frame_width)
                #double_click(index_finger,middle_finger,frame_height,frame_width)
                scroll(y_index,frame_height)
                x_thumb=int(thumb_finger.x*frame_width)
                y_thumb=int(thumb_finger.y*frame_height)



                distance_middle_thumb = math.hypot(
                    (thumb_finger.x - middle_finger.x)*frame_width,
                    (thumb_finger.y - middle_finger.y) * frame_height
                )

                distance_thumb_pinky = abs(thumb_finger.x - pinky_finger.x) * frame_width

                distance_index_thumb = math.hypot(
                    (index_finger.x - thumb_finger.x)*frame_width,
                    (index_finger.y - thumb_finger.y)*frame_height
                )

                distance_ring_thumb = math.hypot((ring_finger.x- thumb_finger.x)*frame_width,
                                                 (ring_finger.x - thumb_finger.y)*frame_height
                )
                print(distance_ring_thumb)

                current_time = time.time()
                if distance_middle_thumb < 70 and (current_time - last_time > 2):
                    last_time=current_time
                    threading.Thread(target=thanos_snap,daemon=True).start()


                elif distance_thumb_pinky < 40 and (current_time - last_time > 2):
                    last_time=current_time
                    threading.Thread(target=minimize(),daemon=True).start()
                    print("dis: ", distance_thumb_pinky)


                elif distance_index_thumb < 30:
                    increase_volume()

                 #if distance_ring_thumb < 30:
                #     decrease_volume()
        volume_bar(current_volume)

        cv2.imshow('Camera', frame)
        if cv2.waitKey(8) & 0xFF == ord('q'):
            break
finally:
    # Release resources and cleanup
    hands.close()  # Cleanup Mediapipe Hands object
    camera.release()
    cv2.destroyAllWindows()





