<br />
<p align="center">
  <h3 align="center">Virtual Steering Wheel</h3>
  <p align="center">
    A virtual steering wheel, made with Python and pre-trained machine learning models. 
  </p>
</p>


<!-- ABOUT THE PROJECT -->
## About The Project

Recently got a webcam, and I've always wanted to explore using it to play around with computer vision (e.g., hand and gesture tracking); so I decided to create a virtual steering wheel with Python.

## How it Works
Uses Python (OpenCV) and the pre-trained models from [Mediapipe (Google)](http://google.github.io/mediapipe/ "Mediapipe (Google)") to capture video, recognize hands in the frame and then calculate the slope between the two hands to determine which direction to turn in. 

Welcome to the Virtual ML Steering Wheel project! This project leverages the power of OpenCV and machine learning techniques to create a virtual steering wheel interface for controlling applications and games.

By utilizing OpenCV's computer vision capabilities, this project enables users to interact with virtual steering controls in real-time using gestures captured through a webcam. The integration of machine learning algorithms enhances the accuracy and responsiveness of the steering controls, providing a seamless and intuitive user experience.

Key Features:

Real-time gesture recognition: The project employs OpenCV to detect and recognize hand gestures captured by a webcam, allowing users to interact with the virtual steering controls effortlessly.
Machine learning-based steering prediction: Through the implementation of machine learning models, the system predicts the intended steering direction based on the detected hand gestures, ensuring smooth and precise control.
Customizable interface: Users have the flexibility to customize the appearance and behavior of the virtual steering wheel to suit their preferences and application requirements.
Compatibility: The project is designed to be compatible with various platforms and applications, making it adaptable for a wide range of use cases, including gaming, simulations, and interactive applications.

CODE : 

#importing libraries
import cv2
import mediapipe as mp
from pynput.keyboard import Key, Controller

#setting up mediapipe functions
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

#assigning keyboard as controller
keyboard = Controller()

#setting up capturing of hand and tracking
cap = cv2.VideoCapture(0)
with mp_hands.Hands(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
) as hands:
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            continue

        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        results = hands.process(image)
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    image,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS
                )

                #setting up co ordinates for straight,right and left
                x_coords = [landmark.x for landmark in hand_landmarks.landmark]
                mean_x = sum(x_coords) / len(x_coords)
                if mean_x < 0.4:
                    print("Turn left.")
                    keyboard.release('s')
                    keyboard.release('d')
                    keyboard.press('a')
                elif mean_x > 0.6:
                    print("Turn right.")
                    keyboard.release('s')
                    keyboard.release('a')
                    keyboard.press('d')
                else:
                    print("Keeping straight.")
                    keyboard.release('a')
                    keyboard.release('d')
                    keyboard.press('w')
                    

        cv2.imshow('Hand Tracking', image)

        #assigning break key as 'q'
        if cv2.waitKey(5) & 0xFF == ord('q'):
            break

#terminating program
cap.release()
cv2.destroyAllWindows()
