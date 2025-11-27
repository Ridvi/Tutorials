import cv2
import mediapipe as mp
import pyautogui
import math
import time
import numpy as np
import threading
from Quartz.CoreGraphics import CGDisplayIOServicePort, IOServiceRequestProbe
from Quartz import CGDisplayMainDisplay
import IOKit
import IOKit.i2c

# Get screen size
screen_width, screen_height = pyautogui.size()

# Initialize Mediapipe Face Detection
mp_face = mp.solutions.face_mesh
face = mp_face.FaceMesh(min_detection_confidence=0.5, min_tracking_confidence=0.5)

# Initialize Mediapipe Hand Detection
mp_hand = mp.solutions.hands
hands = mp_hand.Hands(
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)
mp_draw = mp.solutions.drawing_utils

# Initialize Camera
camera = cv2.VideoCapture(0)
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

last_time = 0
prev_x, prev_y = 0, 0


def thanos_snap():
    pyautogui.hotkey('command', 'q')


def minimize():
    pyautogui.hotkey('command', 'm')


def hand_tips():
    index_finger = hand_landmarks.landmark[mp_hand.HandLandmark.INDEX_FINGER_TIP]
    thumb_finger = hand_landmarks.landmark[mp_hand.HandLandmark.THUMB_TIP]
    thumb_base = hand_landmarks.landmark[mp_hand.HandLandmark.THUMB_CMC]
    middle_finger = hand_landmarks.landmark[mp_hand.HandLandmark.MIDDLE_FINGER_TIP]
    pinky_finger = hand_landmarks.landmark[mp_hand.HandLandmark.PINKY_TIP]

    return index_finger, thumb_finger, thumb_base, middle_finger, pinky_finger


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


# Brightness functions using pyobjc on macOS
def get_brightness():
    """Get the current brightness level."""
    try:
        displayID = CGDisplayMainDisplay()
        io_service_port = CGDisplayIOServicePort(displayID)
        brightness = IOKit.IODisplayGetFloatParameter(
            io_service_port,
            IOKit.kIODisplayBrightnessKey,
            1.0
        )
        return brightness
    except Exception as e:
        print(f"Failed to retrieve brightness: {e}")
        return 0.5


def set_brightness(level):
    """Set the brightness level."""
    try:
        displayID = CGDisplayMainDisplay()
        io_service_port = CGDisplayIOServicePort(displayID)
        IOKit.IODisplaySetFloatParameter(
            io_service_port,
            IOKit.kIODisplayBrightnessKey,
            level
        )
    except Exception as e:
        print(f"Failed to set brightness: {e}")


current_brightness = get_brightness()
brightness_level = 0.5
last_smile_time = time.time()

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

        if results_face.multi_face_landmarks:
            print("face")
            for face_landmarks in results_face.multi_face_landmarks:
                upper_lip = face_landmarks.landmark[13]
                lower_lip = face_landmarks.landmark[14]
                left_corner = face_landmarks.landmark[61]
                right_corner = face_landmarks.landmark[291]

                # Convert normalized coordinates to pixels
                upper_lip_y = int(upper_lip.y * frame_height)
                lower_lip_y = int(lower_lip.y * frame_height)
                left_corner_x = int(left_corner.x * frame_width)
                right_corner_x = int(right_corner.x * frame_width)

                # Compute smile parameters
                smile_width = right_corner_x - left_corner_x
                smile_height = lower_lip_y - upper_lip_y

                # Detect smiling and adjust brightness
                if smile_width > 2.5 * abs(smile_height):
                    if current_brightness < 1.0:  # Max brightness = 1.0
                        current_brightness += 0.05  # Gradually increase
                        set_brightness(current_brightness)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                draw_landmarks(frame, hand_landmarks)
                index_finger, thumb_finger, thumb_base, middle_finger, pinky_finger = hand_tips()
                y_index = move(index_finger, frame_width, frame_height)

        # Display the frame
        cv2.imshow('Camera', frame)
        if cv2.waitKey(8) & 0xFF == ord('q'):
            break
finally:
    # Release resources and cleanup
    hands.close()  # Cleanup Mediapipe Hands object
    camera.release()
    cv2.destroyAllWindows()