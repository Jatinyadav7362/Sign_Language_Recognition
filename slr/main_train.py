print("INFO: Initializing System")
import copy
import cv2 as cv
import mediapipe as mp
from dotenv import load_dotenv
from slr.utils.args import get_args
from slr.utils.landmarks import draw_landmarks
from slr.utils.draw_debug_train import draw_bounding_rect
from slr.utils.draw_debug_train import draw_hand_label
from slr.utils.pre_process_train import calc_bounding_rect
from slr.utils.pre_process_train import calc_landmark_list
from slr.utils.pre_process_train import pre_process_landmark
from slr.utils.logging import log_keypoints
from slr.utils.logging import get_dict_form_list


def main_train():
    #: -
    #: Getting all arguments
    load_dotenv()
    args = get_args()

    keypoint_file = "slr/model/keypoint.csv"
    counter_obj = get_dict_form_list(keypoint_file)

    #: cv Capture
    CAP_DEVICE = args.device
    CAP_WIDTH = args.width
    CAP_HEIGHT = args.height

    #: mp Hands
    # USE_STATIC_IMAGE_MODE = args.use_static_image_mode
    USE_STATIC_IMAGE_MODE = True
    MAX_NUM_HANDS = args.max_num_hands
    MIN_DETECTION_CONFIDENCE = args.min_detection_confidence
    MIN_TRACKING_CONFIDENCE = args.min_tracking_confidence

    #: Drawing Rectangle
    # USE_BRECT = args.use_brect
    MODE = 1
    # DEBUG = int(os.environ.get("DEBUG", "0")) == 1
    CAP_DEVICE = 0

    print("INFO: System initialization Successful")
    print("INFO: Opening Camera")

    #: -
    #: Capturing image
    cap = cv.VideoCapture(CAP_DEVICE)
    cap.set(cv.CAP_PROP_FRAME_WIDTH, CAP_WIDTH)
    cap.set(cv.CAP_PROP_FRAME_HEIGHT, CAP_HEIGHT)

    #: -
    #: Setup hands
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(
        static_image_mode=USE_STATIC_IMAGE_MODE,
        max_num_hands=MAX_NUM_HANDS,
        min_detection_confidence=MIN_DETECTION_CONFIDENCE,
        min_tracking_confidence=MIN_TRACKING_CONFIDENCE,
    )

    print("INFO: System is up & running")
    #: -
    #: Main Loop Start Here...
    while True:

        #: -
        #: Setup Quit key for program
        key = cv.waitKey(1)
        if key == 27:  # ESC key
            print("INFO: Exiting...")
            break

        #: -
        #: Camera capture
        success, image = cap.read()
        if not success:
            continue

        image = cv.resize(image, (CAP_WIDTH, CAP_HEIGHT))

        #: Flip Image for mirror display
        image = cv.flip(image, 1)
        debug_image = copy.deepcopy(image)

        #: Converting to RBG from BGR
        image = cv.cvtColor(image, cv.COLOR_BGR2RGB)

        image.flags.writeable = False
        results = hands.process(image)  #: Hand's landmarks
        image.flags.writeable = True

        #: -
        #: Start Detection
        if results.multi_hand_landmarks is not None:
            for hand_landmarks, handedness in zip(
                results.multi_hand_landmarks, results.multi_handedness
            ):

                #: Calculate  BoundingBox
                use_brect = True
                brect = calc_bounding_rect(debug_image, hand_landmarks)

                #: Landmark calculation
                landmark_list = calc_landmark_list(debug_image, hand_landmarks)

                #: Conversion to relative coordinates / normalized coordinates
                pre_processed_landmark_list = pre_process_landmark(landmark_list)

                if MODE == 1:  #: Logging Mode
                    log_keypoints(
                        key, pre_processed_landmark_list, counter_obj, data_limit=1000
                    )

                #: -
                #: Drawing debug info
                debug_image = draw_bounding_rect(debug_image, use_brect, brect)
                debug_image = draw_landmarks(debug_image, landmark_list)
                debug_image = draw_hand_label(debug_image, brect, handedness)

        cv.imshow("Sign Language Recognition", debug_image)

    cap.release()
    cv.destroyAllWindows()

    print("INFO: Bye")


if __name__ == "__main__":
    main_train()
