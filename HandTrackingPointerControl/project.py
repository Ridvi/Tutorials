import cv2
import mediapipe as mp
import math
import subprocess

# Initialize Mediapipe Hand Detection
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# Initialize Camera
camera = cv2.VideoCapture(0)

# Get Current Volume Level
def get_volume():
    result = subprocess.run(["osascript", "-e", "output volume of (get volume settings)"], capture_output=True, text=True)
    return int(result.stdout.strip())

# Function to increase volume
def increase_volume():
    subprocess.run(["osascript", "-e", "set volume output volume (output volume of (get volume settings) + 10)"])

# Function to decrease volume
def decrease_volume():
    subprocess.run(["osascript", "-e", "set volume output volume (output volume of (get volume settings) - 10)"])

while True:
    ret, frame = camera.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    current_volume = get_volume()  # Get the current volume level

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Get landmark positions
            index_finger = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            middle_finger = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
            ring_finger = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP]
            thumb_finger = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]

            frame_height, frame_width, _ = frame.shape

            # Convert normalized coordinates to pixel values
            def get_position(finger):
                return int(finger.x * frame_width), int(finger.y * frame_height)

            x_index, y_index = get_position(index_finger)
            x_ring, y_ring = get_position(ring_finger)
            x_thumb, y_thumb = get_position(thumb_finger)


            distance_index_thumb = math.hypot(x_index - x_thumb, y_index - y_thumb)
            distance_ring_thumb = math.hypot(x_ring - x_thumb, y_ring - y_thumb)


            if distance_index_thumb < 30:
                increase_volume()

            elif distance_ring_thumb < 30:
                decrease_volume()


    # Draw Volume Indicator
    bar_x, bar_y = 50, 50  # Position of the bar
    bar_height = 200
    max_volume = 100  # Maximum volume
    bar_fill = int((current_volume / max_volume) * bar_height)

    cv2.rectangle(frame, (bar_x, bar_y), (bar_x + 40, bar_y + bar_height), (255, 255, 255), 2)  # Outline
    cv2.rectangle(frame, (bar_x, bar_y + (bar_height - bar_fill)), (bar_x + 40, bar_y + bar_height), (0, 255, 0), -1)  # Filled part
    cv2.putText(frame, f"Volume: {current_volume}%", (bar_x, bar_y + bar_height + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    # Display the frame
    cv2.imshow("Hand Gesture Volume Control", frame)

    # Press 'q' to exit
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

camera.release()
cv2.destroyAllWindows()
