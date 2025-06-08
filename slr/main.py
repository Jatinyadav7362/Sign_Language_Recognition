import csv
import time
import cv2 as cv
import mediapipe as mp
from slr.model.classifier import KeyPointClassifier
from slr.utils.landmarks import draw_landmarks
from slr.utils.draw_debug import draw_bounding_rect, draw_hand_label
from slr.utils.pre_process import calc_bounding_rect, calc_landmark_list, pre_process_landmark

# Initialize MediaPipe Hand model
mp_hands = mp.solutions.hands.Hands(
    static_image_mode=False, max_num_hands=1, 
    min_detection_confidence=0.5, min_tracking_confidence=0.5
)

# Load trained KeyPoint Classifier model
keypoint_classifier = KeyPointClassifier()
keypoint_labels_file = "slr/model/label.csv"
keypoint_classifier_labels = []

with open(keypoint_labels_file, encoding="utf-8-sig") as f:
    keypoint_classifier_labels = [row[0] for row in csv.reader(f)]

# Global variables for sentence formation
detected_sentence = ""
last_word_time = None  # This will be set when first detection happens
first_detection = True  # Track if the first word has been detected

def process_frame(image):
    global detected_sentence, last_word_time, first_detection
    image = cv.flip(image, 1)  # Mirror effect for user-friendly interaction
    image_rgb = cv.cvtColor(image, cv.COLOR_BGR2RGB)
    results = mp_hands.process(image_rgb)
    image = cv.cvtColor(image_rgb, cv.COLOR_RGB2BGR)

    current_time = time.time()

    # If no word has been detected yet, start the first detection timer
    if last_word_time is None:
        last_word_time = current_time

    required_time = 7 if first_detection else 4  # 15s for first, 4s for others
    remaining_time = max(0, int(required_time - (current_time - last_word_time)))  # Calculate countdown

    if results.multi_hand_landmarks:
        for idx, hand_landmarks in enumerate(results.multi_hand_landmarks):
            # Get hand type (Right or Left)
            handedness = results.multi_handedness[idx].classification[0].label if results.multi_handedness else "Unknown"

            # If Left Hand is detected, display "Wrong Hand" and skip further processing
            if handedness == "Left":
                cv.putText(image, "Wrong Hand", (10,64), cv.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 2, cv.LINE_AA)
                continue  # Skip sign detection for the left hand

            # Calculate bounding box and keypoints
            brect = calc_bounding_rect(image, hand_landmarks)
            landmark_list = calc_landmark_list(image, hand_landmarks)
            pre_processed_landmark_list = pre_process_landmark(landmark_list)
            hand_sign_id = keypoint_classifier(pre_processed_landmark_list)

            # Get predicted sign word
            hand_sign_text = "" if hand_sign_id == 26 else keypoint_classifier_labels[hand_sign_id]

            # Only add the word if the required time has passed
            if hand_sign_text and remaining_time == 0:
                detected_sentence += hand_sign_text + ""
                last_word_time = current_time  # Reset timer
                first_detection = False  # First word has been detected

            # Draw overlays
            image = draw_bounding_rect(image, True, brect)
            image = draw_landmarks(image, landmark_list)
            image = draw_hand_label(image, brect, handedness)  # Show Right/Left Hand

            # Show detected word in the camera feed
            if hand_sign_text:
                cv.putText(image, hand_sign_text, (40, 75), cv.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 3, cv.LINE_AA)

    #  Display countdown timer on the screen
    timer_text = f"{remaining_time}s"
    cv.putText(image, timer_text, (570, 55), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv.LINE_AA)

    return image, detected_sentence


def reset_detected_sentence():
    """Clears the detected sentence and resets the timing logic."""
    global detected_sentence, first_detection, last_word_time
    detected_sentence = ""  # Reset sentence
    first_detection = True  # Ensure first word delay works correctly
    last_word_time = None  # Reset timing logic
    
    
    # In main.py

def delete_last_character():
    global detected_sentence
    if detected_sentence:
        detected_sentence = detected_sentence[:-1]  # Remove last character
