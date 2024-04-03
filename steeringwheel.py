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