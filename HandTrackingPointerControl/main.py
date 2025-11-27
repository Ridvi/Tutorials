import cv2
import mediapipe as mp
import pyautogui
import math
import time
import threading


#Get screen size
screen_width, screen_height = pyautogui.size()

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
def thanos_snap():
    pyautogui.hotkey('command','q')

def minimize():
    pyautogui.hotkey('command','m')

try:
    while True:
        ret, frame = camera.read()
        if not ret:
            print("Failed to grab frame.")
            break

        # Flip the frame and convert to RGB
        frame = cv2.flip(frame, 1)
        frame_height, frame_width, _ = frame.shape
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        #
        results = hands.process(rgb_frame)
        # Define thick drawing specs

        landmark_drawing_spec = mp_draw.DrawingSpec(color=(0, 0, 255), thickness=2, circle_radius=1)  # Thicker points
        connection_drawing_spec = mp_draw.DrawingSpec(color=(0, 255, 0), thickness=2)
        prev_x, prev_y = 0, 0

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_draw.draw_landmarks(
                    frame,
                    hand_landmarks,
                    mp_hand.HAND_CONNECTIONS,
                    landmark_drawing_spec,
                    connection_drawing_spec
                )

                index_finger =hand_landmarks.landmark[mp_hand.HandLandmark.INDEX_FINGER_TIP]
                thumb_finger=hand_landmarks.landmark[mp_hand.HandLandmark.THUMB_TIP]
                thumb_base = hand_landmarks.landmark[mp_hand.HandLandmark.THUMB_CMC]
                middle_finger=hand_landmarks.landmark[mp_hand.HandLandmark.MIDDLE_FINGER_TIP]
                pinky_finger = hand_landmarks.landmark[mp_hand.HandLandmark.PINKY_TIP]

                x_index=int(index_finger.x*frame_width)
                y_index=int(index_finger.y*frame_height)
                x_thumb=int(thumb_finger.x*frame_width)
                y_thumb=int(thumb_finger.y*frame_height)
                screen_x=int(x_index*screen_width/frame_width)*2
                screen_y=int(y_index*screen_height/frame_height)*2

                # smooth_x=int((1-0.1) * screen_x + 0.1 * screen_x)
                # smooth_y=int((1-0.1) * screen_y + 0.1 * screen_y)
                # pyautogui.moveTo(smooth_x, smooth_y,duration=0.001)

                # Smoothing factor (0.2 makes movement smoother, adjust if needed)
                SMOOTHING = 0.6
                # Apply smoothing
                prev_x = prev_x * (1 - SMOOTHING) + screen_x * SMOOTHING
                prev_y = prev_y * (1 - SMOOTHING) + screen_y * SMOOTHING

                pyautogui.moveTo(int(prev_x), int(prev_y), duration=0.001)

                # Measure the distance between thumb tip and thumb base
                distance_thumb = math.hypot(
                    (thumb_finger.x - thumb_base.x) * frame_width,
                    (thumb_finger.y - thumb_base.y) * frame_height
                )
                distance_middle_thumb = math.hypot(
                    (thumb_finger.x - middle_finger.x)*frame_width,
                    (thumb_finger.y - middle_finger.y) * frame_height
                )

                distance_thumb_pinky = abs(thumb_finger.x - pinky_finger.x) * frame_width

                print(f"Thumb distance: {distance_thumb}")
                cv2.putText(
                    frame,  # frame to draw on
                    f'Distance: {int(distance_thumb)}',  # text to show
                    (50, 50),  # position
                    cv2.FONT_HERSHEY_SIMPLEX,  # font
                    1,  # font scale
                    (255, 0, 0),  # color in BGR
                    2  # thickness
                )

                # If thumb is folded (distance is small), perform a click
                if distance_thumb <87:   # Adjust threshold for sensitivity
                    pyautogui.click()

                current_time = time.time()
                if distance_middle_thumb < 70 and (current_time - last_time > 2):
                    last_time=current_time
                    threading.Thread(target=thanos_snap,daemon=True).start()


                if distance_thumb_pinky < 100 and (current_time - last_time > 2):
                    last_time=current_time
                    threading.Thread(target=minimize(),daemon=True).start()



                SCROLL_THRESHOLD = 100  # Adjust this value to change scroll sensitivity

                # Check if the index finger moves significantly up or down
                if y_index < (frame_height // 2 - SCROLL_THRESHOLD):  # Move UP to scroll UP
                    pyautogui.scroll(2)
                elif y_index > (frame_height // 2 ):  # Move DOWN to scroll DOWN
                    pyautogui.scroll(-2)





        # Display the frame
        cv2.imshow('Camera', frame)
        if cv2.waitKey(8) & 0xFF == ord('q'):
            break
finally:
    # Release resources and cleanup
    hands.close()  # Cleanup Mediapipe Hands object
    camera.release()
    cv2.destroyAllWindows()





