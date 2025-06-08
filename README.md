<!-- ![MasterHead](docs/SLR.png)  -->
# Signovate – Real-Time Sign Language Recognition System

This repository contains the source code and resources for **Signovate**, a real-time sign language recognition system. The goal of this project is to bridge the communication gap for individuals with hearing impairments using computer vision and machine learning.

Signovate can recognize sign language gestures in real time and is fully customizable to support any hand gesture recognition task.

## Table of Contents
1. [Introduction](#introduction)
2. [Installation](#installation)
3. [Usage](#usage)
4. [Customization](#customization)
5. [System Overview](#system-overview)
6. [Data Collection](#data-collection)
7. [Preprocessing](#preprocessing)
8. [Model Training](#model-training)
9. [Results](#results)
10. [Screenshots](#screenshots)
11. [Contributing](#contributing)

## Introduction
Sign language is a visual means of communication used by individuals with hearing impairments. This project aims to bridge the communication gap by developing an automated system that can understand and interpret sign language gestures. The system utilizes computer vision techniques and machine learning algorithms to recognize and translate these gestures into text or speech.

The Sign Language Recognition System consists of several components:

- **Data Collection:** A dataset of sign language gestures is collected, including various hand shapes.

- **Preprocessing:** The collected data is preprocessed to enhance the quality, remove noise, and extract relevant features.

- **Model Training:** Machine learning models, specifically convolutional neural networks (CNNs), are trained on the preprocessed data to learn the mapping between input gestures and their corresponding meanings.

- **Real-time Recognition:** The trained model is deployed in a real-time environment, where it takes video input and performs gesture recognition on the fly.

- **Text-to-Speech:** The recognized gestures are converted to text and can be spoken aloud using the speech synthesis functionality.

- **Text Translation:** The system allows building complete sentences with recognized signs, with options to edit and manipulate the text.

## Installation
To set up the Sign Language Recognition System on your local machine, follow these steps:

1. Clone the repository to your local machine:
   
    ```bash
    git clone https://github.com/Jatinyadav7362/Sign_Language_Recognition.git
    ```

2. Install the required packages using the requirements.txt file:
   This project requires **Python 3.10.6**. Please make sure it's installed before proceeding.

    ```bash
    # Windows
    cd Sign_Language_Recognition
    virtualenv env
    .\env\Scripts\activate
    pip install -r requirements.txt

    # Linux/macOS
    cd Sign_Language_Recognition
    virtualenv env
    source env/bin/activate
    pip3 install -r requirements.txt
    ```

You are now ready to use the Sign Language Recognition System on your local machine.


## Usage
To use the Sign Language Recognition System, follow these steps:

1. Ensure that the required dependencies and resources are properly installed and set up.

2. Run the main application:
    ```bash
    python app.py
    ```

3. The application will open a web interface at http://localhost:5000/

4. Navigate to the Translator page to access the main functionality

5. Position your hands clearly in front of the camera

6. Perform ASL gestures to see them translated in real-time

7. Use the control buttons to:
   - Pause/Resume recognition
   - Speak the translated text aloud
   - Clear all recognized text
   - Delete the last recognized character

Here is a demo of the Sign Language Recognition System in action:

<img alt="Signovate Demo" width="45%" src="docs/demo.png">

## Customization
The Sign Language Recognition System is fully customizable and can be trained to recognize any hand gesture. To customize the system, follow these steps:

1. There are two files `app.py` for prediction mode and `app_train.py` for data collection mode.
2. Run the `app.py` file to open the application for prediction mode .
3. For creating your own dataset from scratch reset the keypoint.csv file and counter.json.
4. For creating your own dataset and training it run the `app_train.py` file.
5. Make the hand gesture you want to add to the dataset.
6. Press the alphabetic key to save the gesture to the dataset corresponding to the letter and spacbar key  for space.
7. Add as many gestures as you want to the dataset. More data will result in better accuracy.
8. After adding all the gestures, press the `esc` key to quit the program. Then run the `training.ipynb` Jupyter notebook file to train the model on the new dataset.
   
Enjoy your customized Sign Language Recognition System!

## System Overview
In order to build such systems, data (keypoints of hands) must be obtained, then features involved in sign making must be extracted and finally combination of features must be analyzed to describe the performed sign.

The web application is built using Flask, with a responsive frontend developed using HTML, CSS, and JavaScript. The system includes features for real-time video processing, sign language recognition, text output, and speech synthesis.

![System Overview](docs/flow-chart.png)

## Data Collection
The first step in building a sign language recognition system is to collect a dataset of sign language gestures. The dataset is used to train the machine learning model to recognize and interpret these gestures.

For this project, we use our hand sign data. The data is collected using the [MediaPipe](https://google.github.io/mediapipe/) library. The library provides a hand tracking solution that can detect and track 21 hand landmarks in real-time. The hand landmarks are the key points or 2D coordinates that can be used to determine the pose of the hand.

![Hand Landmarks](docs/hand-landmarks.png)

The hand landmarks are used to extract features from the hand gestures. The features are then used to train a machine learning model to recognize and interpret these gestures.

## Preprocessing
The collected data is preprocessed to enhance the quality, remove noise, and extract relevant features. The preprocessing steps include:

1. Getting the hand landmarks from the video stream.

2. Converting the hand landmarks relative to the `wrist` landmark's coordinate `(0, 0)`. This is done by subtracting the `wrist` landmark's coordinate from all the other landmarks.

   ![Hand Landmarks](docs/hand_landmarks_o_r.png)

3. Flatten the normalized hand landmarks to a 1-dimensional list:

    ```python
    # Convert into a one-dimensional list
    temp_landmark_list = list(itertools.chain.from_iterable(temp_landmark_list))
    ```

4. Normalizing the hand landmarks from `-1` to `1` value:

    ```python
    # Normalize the hand landmarks to a fixed size
    # Normalization (-1 to 1)
    max_value = max(list(map(abs, temp_landmark_list)))

    def normalize_(n):
        return n / max_value

    landmark_list = list(map(normalize_, temp_landmark_list))
    ```

5. Adding the normalized hand landmarks to the dataset:

    ```python
    # Writing dataset
    with open("slr/model/keypoint.csv", 'a', newline="") as f:
        writer = csv.writer(f)
        writer.writerow([index, *landmark_list])
    ```

## Model Training
The preprocessed data is used to train a machine learning model to recognize and interpret sign language gestures. The model is trained using a convolutional neural network (CNN) architecture. The CNN is trained on the preprocessed data to learn the mapping between input gestures and their corresponding meanings.

1. Obtain or create a sign language dataset.

2. Split the dataset into training and validation sets. It is recommended to use a separate testing set for final evaluation.

3. Choose an appropriate machine learning algorithm or architecture, such as CNNs, RNNs, or their combinations, and implement it using a suitable framework like TensorFlow or PyTorch. For this project, we use a ANN architecture implemented using TensorFlow.

4. Train the model using the training dataset and tune hyperparameters to achieve optimal performance.

5. Validate the model using the validation dataset and make necessary adjustments to improve accuracy and generalization.

6. Test the final model using the testing dataset and evaluate its performance using appropriate metrics.

## Results
The model was trained on a dataset of 25,000 hand gestures. The dataset was split into training and validation sets with a ratio of 75:25. The model was trained for 125 epochs with a batch size of 128. The training and validation accuracy and loss were recorded for each epoch.

Our proposed model achieved an accuracy of `75.12%` on the validation set and `94.60%` on the testing set. The model was able to recognize and interpret sign language gestures in real-time with an accuracy of `80.12%`.

The web application successfully integrates this model with a Flask backend and responsive frontend, providing a seamless experience for users. The text-to-speech functionality enables complete two-way communication, allowing the signs to be not only translated to text but also spoken aloud.

## Screenshots
### Welcome Page
![Welcome Page](docs/home.png)

### Translator in Action
![Translator in Action](docs/translator.png)

### About Signovate
![About Signovate](docs/details.png)

### Our Team
![Our Team](docs/contact.png)







## Contributing
Contributions to this project are welcome. If you encounter any issues or have suggestions for improvements, please open an issue or submit a pull request. Let's work together to make the Sign Language Recognition System even better!

We appreciate your contributions, whether big or small, and we look forward to working together to enhance the Sign Language Recognition System. Let's make a positive impact on the lives of individuals with hearing impairments and promote inclusivity in communication.
