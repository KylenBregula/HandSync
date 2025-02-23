"""
Developers: Kylen Bregula, Amber Jones, Isaiah Herard, Katharine Ringo
Date: 22/22/2025
Purpose: This software uses OpenCV to allow camera access via python and the Mediapipe library to detect hands from the camera.
         This is for Demonstration for a surgeon to use hand gestures for easy to access functions during operation.
         However this software can be applied to elsewhere outside that field.
"""
# Imported libraries
# Image processing
import cv2
# Hand Tracking
import mediapipe as mp
# Automating keyboard / mouse events
import pyautogui
# Timed Delays
import time 

# modules imported from mediapipe
# detects the hands
hands_tracking = mp.solutions.hands
# visualizes the hands when detected
hands_drawing = mp.solutions.drawing_utils
# aids in making the visuals from drawing_utils to be more consise
hands_drawing_aid = mp.solutions.drawing_styles

# Global variables 
# Number determines what camera is currently being used
camera = 0

# Initialize default values
last_guide_position = None  
last_light_position = None  
recording = False  
gesture_threshold = 0.05

# Saves the time of the last recorded toggle
# This prevents rapid state changes for gestures
last_state_time = time.time()
# Delay in seconds (can be adjusted as needed)
one_second_delay = 1.0  

# Webcam input
video = cv2.VideoCapture(camera)

# Hand Signals (more can be added for additional functionality)
# Uses hand_landmarks to determine fingers closing
# hand_landmarks is from Mediapipe in which a hand as 21 points attached to it. These points are located with the given documentation
# All gestures have thumb out so to promote modularity we have this method to detect if the thumb is extended
# Name scheme represents the fingers that are extended
def thumb_up(hand_landmarks):
    
    # Gets thumb points from hand_landmarks mediapipe library
    thumb_tip = hand_landmarks.landmark[hands_tracking.HandLandmark.THUMB_TIP]
    thumb_ip = hand_landmarks.landmark[hands_tracking.HandLandmark.THUMB_IP]
    thumb_mcp = hand_landmarks.landmark[hands_tracking.HandLandmark.THUMB_MCP]

    # Compares the thumb points and if the tip is lower then returns true due to it being extended
    return (thumb_tip.y < thumb_ip.y) and (thumb_ip.y < thumb_mcp.y)

def thumb_out(hand_landmarks):
  
    # Gets thumb points from thumb_up method
    thumb_extended = thumb_up(hand_landmarks)

    # Gets index points from hand_landmarks mediapipe library
    index_tip = hand_landmarks.landmark[hands_tracking.HandLandmark.INDEX_FINGER_TIP]
    index_pip = hand_landmarks.landmark[hands_tracking.HandLandmark.INDEX_FINGER_PIP]

    # Gets middle points from hand_landmarks mediapipe library
    middle_tip = hand_landmarks.landmark[hands_tracking.HandLandmark.MIDDLE_FINGER_TIP]
    middle_pip = hand_landmarks.landmark[hands_tracking.HandLandmark.MIDDLE_FINGER_PIP]

    # Gets ring points from hand_landmarks mediapipe library
    ring_tip = hand_landmarks.landmark[hands_tracking.HandLandmark.RING_FINGER_TIP]
    ring_pip = hand_landmarks.landmark[hands_tracking.HandLandmark.RING_FINGER_PIP]

    # Gets pinky points from hand_landmarks mediapipe library
    pinky_tip = hand_landmarks.landmark[hands_tracking.HandLandmark.PINKY_TIP]
    pinky_pip = hand_landmarks.landmark[hands_tracking.HandLandmark.PINKY_PIP]

    # Ensure other fingers are down with a threshold
    other_fingers_down = (index_tip.y > index_pip.y + gesture_threshold) and (middle_tip.y > middle_pip.y + gesture_threshold) and (ring_tip.y > ring_pip.y + gesture_threshold) and (pinky_tip.y > pinky_pip.y + gesture_threshold)

    # Checks if thumb extended and all other fingers down
    # Compares bool values together so both must be true be recognized as gesture
    return thumb_extended and other_fingers_down

def thumb_pinky_out(hand_landmarks):

    # Gets thumb points from thumb_up method
    thumb_extended = thumb_up(hand_landmarks)

    # Gets index points from hand_landmarks mediapipe library
    index_tip = hand_landmarks.landmark[hands_tracking.HandLandmark.INDEX_FINGER_TIP]
    index_pip = hand_landmarks.landmark[hands_tracking.HandLandmark.INDEX_FINGER_PIP]

    # Gets middle points from hand_landmarks mediapipe library
    middle_tip = hand_landmarks.landmark[hands_tracking.HandLandmark.MIDDLE_FINGER_TIP]
    middle_pip = hand_landmarks.landmark[hands_tracking.HandLandmark.MIDDLE_FINGER_PIP]

    # Gets ring points from hand_landmarks mediapipe library
    ring_tip = hand_landmarks.landmark[hands_tracking.HandLandmark.RING_FINGER_TIP]
    ring_pip = hand_landmarks.landmark[hands_tracking.HandLandmark.RING_FINGER_PIP]

    # Gets pinky points from hand_landmarks mediapipe library
    pinky_tip = hand_landmarks.landmark[hands_tracking.HandLandmark.PINKY_TIP]
    pinky_pip = hand_landmarks.landmark[hands_tracking.HandLandmark.PINKY_PIP]
    # Compares the pinky points and if the tip is lower then returns true due to it being extended
    pinky_extended = pinky_tip.y < pinky_pip.y  

    # Ensure other fingers are down with a threshold
    other_fingers_down = (index_tip.y > index_pip.y + gesture_threshold) and (middle_tip.y > middle_pip.y + gesture_threshold) and (ring_tip.y > ring_pip.y + gesture_threshold)

    # Checks if thumb extended and all other fingers down but pinky 
    # Compares bool values together so both must be true be recognized as gesture
    return thumb_extended and pinky_extended and other_fingers_down

def thumb_index_out(hand_landmarks):
  
    # Gets thumb points from thumb_up method
    thumb_extended = thumb_up(hand_landmarks)  # Reuse the thumb_out function

    # Gets index points from hand_landmarks mediapipe library
    index_tip = hand_landmarks.landmark[hands_tracking.HandLandmark.INDEX_FINGER_TIP]
    index_pip = hand_landmarks.landmark[hands_tracking.HandLandmark.INDEX_FINGER_PIP]
    # Compares the index points and if the tip is lower then returns true due to it being extended
    index_extended = index_tip.y < index_pip.y  

    # Gets middle points from hand_landmarks mediapipe library
    middle_tip = hand_landmarks.landmark[hands_tracking.HandLandmark.MIDDLE_FINGER_TIP]
    middle_pip = hand_landmarks.landmark[hands_tracking.HandLandmark.MIDDLE_FINGER_PIP]
    
    # Gets ring points from hand_landmarks mediapipe library
    ring_tip = hand_landmarks.landmark[hands_tracking.HandLandmark.RING_FINGER_TIP]
    ring_pip = hand_landmarks.landmark[hands_tracking.HandLandmark.RING_FINGER_PIP]

    # Gets pinky points from hand_landmarks mediapipe library
    pinky_tip = hand_landmarks.landmark[hands_tracking.HandLandmark.PINKY_TIP]
    pinky_pip = hand_landmarks.landmark[hands_tracking.HandLandmark.PINKY_PIP]

    # Ensure other fingers are down with a threshold
    other_fingers_down = (middle_tip.y > middle_pip.y + gesture_threshold) and (ring_tip.y > ring_pip.y + gesture_threshold) and (pinky_tip.y > pinky_pip.y + gesture_threshold)

    # Checks if thumb extended and all other fingers down but index
    # Compares bool values together so both must be true be recognized as gesture
    return thumb_extended and index_extended and other_fingers_down

def thumb_index_middle_out(hand_landmarks):

    # Gets thumb points from thumb_up method
    thumb_extended = thumb_up(hand_landmarks)  

    # Gets index points from hand_landmarks mediapipe library
    index_tip = hand_landmarks.landmark[hands_tracking.HandLandmark.INDEX_FINGER_TIP]
    index_pip = hand_landmarks.landmark[hands_tracking.HandLandmark.INDEX_FINGER_PIP]
    # Compares the index points and if the tip is lower then returns true due to it being extended
    index_extended = index_tip.y < index_pip.y  

    # Gets middle points from hand_landmarks mediapipe library
    middle_tip = hand_landmarks.landmark[hands_tracking.HandLandmark.MIDDLE_FINGER_TIP]
    middle_pip = hand_landmarks.landmark[hands_tracking.HandLandmark.MIDDLE_FINGER_PIP]
    # Compares the middle points and if the tip is lower then returns true due to it being extended
    middle_extended = middle_tip.y < middle_pip.y 

    # Gets ring points from hand_landmarks mediapipe library
    ring_tip = hand_landmarks.landmark[hands_tracking.HandLandmark.RING_FINGER_TIP]
    ring_pip = hand_landmarks.landmark[hands_tracking.HandLandmark.RING_FINGER_PIP]

    # Gets pinky points from hand_landmarks mediapipe library
    pinky_tip = hand_landmarks.landmark[hands_tracking.HandLandmark.PINKY_TIP]
    pinky_pip = hand_landmarks.landmark[hands_tracking.HandLandmark.PINKY_PIP]

    # Ensure other fingers are down with a threshold
    other_fingers_down = (ring_tip.y > ring_pip.y + gesture_threshold) and (pinky_tip.y > pinky_pip.y + gesture_threshold)

    # Checks if thumb extended and all other fingers down but index, middle
    # Compares bool values together so both must be true be recognized as gesture
    return thumb_extended and index_extended and middle_extended and other_fingers_down

def thumb_index_middle_ring_out(hand_landmarks):
    
    # Access global variables
    global recording, last_state_time 

    # Gets thumb points from thumb_up method
    thumb_extended = thumb_up(hand_landmarks)

    # Gets index points from hand_landmarks mediapipe library
    index_tip = hand_landmarks.landmark[hands_tracking.HandLandmark.INDEX_FINGER_TIP]
    index_pip = hand_landmarks.landmark[hands_tracking.HandLandmark.INDEX_FINGER_PIP]
    # Compares the index points and if the tip is lower then returns true due to it being extended
    index_extended = index_tip.y < index_pip.y  

    # Gets middle points from hand_landmarks mediapipe library
    middle_tip = hand_landmarks.landmark[hands_tracking.HandLandmark.MIDDLE_FINGER_TIP]
    middle_pip = hand_landmarks.landmark[hands_tracking.HandLandmark.MIDDLE_FINGER_PIP]
    # Compares the middle points and if the tip is lower then returns true due to it being extended
    middle_extended = middle_tip.y < middle_pip.y  

    # Gets ring points from hand_landmarks mediapipe library
    ring_tip = hand_landmarks.landmark[hands_tracking.HandLandmark.RING_FINGER_TIP]
    ring_pip = hand_landmarks.landmark[hands_tracking.HandLandmark.RING_FINGER_PIP]
    # Compares the ring points and if the tip is lower then returns true due to it being extended
    ring_extended = ring_tip.y < ring_pip.y  

    # Gets pinky points from hand_landmarks mediapipe library
    pinky_tip = hand_landmarks.landmark[hands_tracking.HandLandmark.PINKY_TIP]
    pinky_pip = hand_landmarks.landmark[hands_tracking.HandLandmark.PINKY_PIP]

     # Ensure other finger is down with a threshold
    pinky_down = pinky_tip.y > pinky_pip.y + gesture_threshold  

    # Check if the gesture is detected and enough time has passed since the last toggle
    # This allows to toggle states between recording and not recording
    current_time = time.time()
    if thumb_extended and index_extended and middle_extended and ring_extended and pinky_down:
        # If delay has passed allow toggle 
        # Waits 1 second
        if current_time - last_state_time > one_second_delay:  
            # Toggle state
            recording = not recording  
            # Update time
            last_state_time = current_time  
    return recording

# Functions (more can be added as needed for the future)
# Simulates a right arrow key
def go_next_slide():

    # Access global variables
    global last_state_time  

    # Allows for 1 second delay
    current_time = time.time()

    # Waits 1 second
    if current_time - last_state_time > one_second_delay:
        # Simulate key press
        pyautogui.press("right")  
        # Update the last key press time
        last_state_time = current_time  

# Simulates a left arrow key
def go_previous_slide():

    # Access global variables
    global last_state_time  

    # Allows for 1 second delay
    current_time = time.time()

    # Waits 1 second
    if current_time - last_state_time > one_second_delay:
        # Simulate key press
        pyautogui.press("left")  
        # Update the last key press time
        last_state_time = current_time  

# When active a red outline Circle follows the index finger. When deactivated leave the red outline Circle in its last known position
def place_guide():

  # Access global variables
  global last_guide_position

  # Gets index points from hand_landmarks mediapipe library
  index_tip = hand_landmarks.landmark[hands_tracking.HandLandmark.INDEX_FINGER_TIP]

  # Gets image size
  h, w, _ = image.shape  

  # Saves last position of guide
  last_guide_position = (int(index_tip.x * w), int(index_tip.y * h))  

# When active a white filled Circle follows the middle finger. When deactivated leave the white filled Circle in its last known position
def place_light():

  # Access global variables
  global last_light_position

  # Gets middle points from hand_landmarks mediapipe library
  middle_tip = hand_landmarks.landmark[hands_tracking.HandLandmark.MIDDLE_FINGER_TIP]

  # Gets image size
  h, w, _ = image.shape  

  # Saves last position of light source
  last_light_position = (int(middle_tip.x * w), int(middle_tip.y * h))  

# A red circle on the top left of the screen appears.
# This is a toggle to demonstrate the recording and unrecording of video. 
# When the videos is recorded the video is sent to a database to be accessed later
def play_stop_record(image):
  
  # Gets image size
  h, w, _ = image.shape  

  # Gets top right screen poition
  top_right_position = (w - 35, 35) 

  # Creates red filled circle top right of screen
  cv2.circle(image, top_right_position, 20, (0, 0, 255), -1) 

# Initializes a MediaPipe hands tracking model using library parameters
# static_image_mode - Tracks hands across video frames 
# max_num_hands - Sets the maximum number of hands the model can detect and track
# model_complexity - Controls the model’s accuracy vs. speed trade-off
# min_detection_confidence - Threshold (60%) for detecting a new hand
# min_tracking_confidence - Threshold (90%) for tracking an already-detected hand.
with hands_tracking.Hands(static_image_mode = False, max_num_hands = 1, model_complexity = 1, min_detection_confidence= 0.6, min_tracking_confidence= 0.9) as hands:
  
  # Loop while the video is open
  while video.isOpened():
    # Read the next frame from the video
    success, image = video.read()
    # If it fails it ignores and continues as normal
    if not success:
      continue  

    # Allows resizing the window manually
    cv2.namedWindow("MediaPipe Hands", cv2.WINDOW_NORMAL)
    # Allows to stay on top of other windows
    cv2.setWindowProperty("MediaPipe Hands", cv2.WND_PROP_TOPMOST, 1)

    # Creates frames to be read only
    # Makes computations for hand detection faster due to unnecessary copying and modifications
    image.flags.writeable = False
    # Converts BGR to RGB for library compatibility
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Detects hands
    hands_found = hands.process(image)

    # Draw hand landmarks if hands are detected
    image.flags.writeable = True
    # Converts BRGBGR to BGR for library compatibility
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    # Check if any hands are detected in the frame
    if hands_found.multi_hand_landmarks:
      # Iterate through each detected hand
      # Draw landmarks and connections on the image
      for hand_landmarks in hands_found.multi_hand_landmarks: hands_drawing.draw_landmarks(image, hand_landmarks, hands_tracking.HAND_CONNECTIONS, hands_drawing_aid.get_default_hand_landmarks_style(), hands_drawing_aid.get_default_hand_connections_style())

      # Where the hand gestures and functions are connected
      # Can be customized to surgeon's liking
      # Once gesture is true it performs the method attached
      if thumb_out(hand_landmarks):
        go_next_slide()

      elif thumb_pinky_out(hand_landmarks):
        go_previous_slide()

      elif thumb_index_out(hand_landmarks):
        place_guide()

      elif thumb_index_middle_out(hand_landmarks):
        place_light()

      elif thumb_index_middle_ring_out(hand_landmarks):
        play_stop_record(image) 

    # Creates white filled circle at last known functions point
    if last_guide_position:
      cv2.circle(image, last_guide_position, 15, (0, 0, 255), 3)  

    # Creates red outline circle at last known functions point
    if last_light_position:
      cv2.circle(image, last_light_position, 20, (255, 255, 255), -1) 
            
    # Outputting Camera Feed
    cv2.imshow('MediaPipe Hands', cv2.flip(image, 1))

    # Checks for key presses
    key = cv2.waitKey(5) & 0xFF
    # Press 'q' to exit program
    if key == ord('q'):  
        break
      
    # '[' key to decrease
    elif key == ord('['):  
        if camera > 0:  
            camera -= 1
            # Disconnects from current camera
            video.release()
            # Reconnects with new camera
            video = cv2.VideoCapture(camera)

    # ']' key to increase
    elif key == ord(']'):  
        camera += 1
        # Disconnects from current camera
        video.release()
        # Reconnects with new camera
        video = cv2.VideoCapture(camera)

# Disconnects from current camera
video.release()
# Closes application
cv2.destroyAllWindows()
