import csv
import cv2 as cv
import json
import numpy as np


def log_keypoints(key, landmark_list, counter_obj, data_limit=1000):
    """
    Logs keypoints when a key is pressed and saves them to a CSV file.

    :param key: Keyboard key (letter or space)
    :param landmark_list: Preprocessed landmark list
    :param counter_obj: Dictionary tracking the count of each label
    :param data_limit: Maximum number of samples per label
    :return: None
    """
    counter_file = "slr/model/counter.json"
    csv_path = "slr/model/keypoint.csv"
    index = -1

    # Avoid logging 'J/j' or 'Z/z'
    if key in [74, 106]:  # ASCII: J/j
        return

    # Handling Spacebar (key == 32)
    if key == 32:
        index = 24  # Assigning space the next available index after Y

    # Handling letters A-Y (excluding J and Z)
    elif 65 <= key <= 89 or 97 <= key <= 121:  # A-Y / a-y
        if 65 <= key <= 90:  # Capital letters
            index = key - 65
            if key > 74:  # Adjust index after J
                index -= 1

        elif 97 <= key <= 122:  # Small letters
            index = key - 97
            if key > 106:  # Adjust index after j
                index -= 1

    # If key is not recognized, return
    if index == -1:
        return

    # Update counter for dataset limit
    if str(index) in counter_obj.keys():
        counter_obj[str(index)] += 1
    else:
        counter_obj[str(index)] = 1

    # Check data limit
    if counter_obj[str(index)] > data_limit:
        print(f"Dataset limit reached for {chr(key).upper() if key != 32 else 'Space'} [{counter_obj[str(index)] - 1}/{data_limit}]")
        return

    # Save counter update
    with open(counter_file, "w") as cf:
        counter_obj_writable = json.dumps(counter_obj, indent=4)
        cf.write(counter_obj_writable)

    # Print logging status
    print(f"{chr(key).upper() if key != 32 else 'Space'} => {counter_obj[str(index)]}/{data_limit}")

    # Write keypoints to CSV
    with open(csv_path, 'a', newline="") as f:
        writer = csv.writer(f)
        writer.writerow([index, *landmark_list])


def get_dict_form_list(file):
    """
    Reads the dataset and counts the occurrences of each label.
    
    :param file: Path to the CSV file
    :return: Dictionary with counts of each label
    """
    _list = []
    with open(file) as f:
        for row in f:
            _list.append(row.split(",")[0])

    if len(_list) == 0:
        return {}

    obj = {}
    set_list = set(_list)

    for i in set_list:
        obj[str(i)] = _list.count(i)

    return obj


def get_mode(key, _mode):
    """
    Toggles between normal mode (0) and logging mode (1) when 0 or 1 is pressed.

    :param key: Pressed key
    :param _mode: Current mode
    :return: Updated mode
    """
    mode = _mode
    if key == 48:  # Key '0'
        mode = 0
    elif key == 49:  # Key '1'
        mode = 1
    return mode
