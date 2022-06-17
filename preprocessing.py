import cv2
import mediapipe as mp
import numpy as np

mp_hands = mp.solutions.hands
draw = mp.solutions.drawing_utils

def hand_extractor(image, w, h):
    hand_points_image = np.zeros((224, 224, 3), np.uint8)
    hand_image = np.zeros((224, 224, 3), np.uint8)
    hand_image_model = np.zeros((224, 224, 3), np.uint8)
    x = -1
    y = -1

    with mp_hands.Hands(
            static_image_mode=True,
            max_num_hands=1,
            min_detection_confidence=0.5) as hands:
        result = hands.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        if result.multi_hand_landmarks:

            for hand_landmarks in result.multi_hand_landmarks:

                x = hand_landmarks.landmark[9].x
                y = hand_landmarks.landmark[9].y

                coef_x = 0.5 - x
                coef_y = 0.5 - y

                hand_points_image = np.zeros((224, 224, 3), np.uint8)

                X_arr = list()
                Y_arr = list()

                for i, point in enumerate(hand_landmarks.landmark):
                    X = int((coef_x + point.x) * 224)
                    Y = int((coef_y + point.y) * 224)

                    X_arr.append(point.x)
                    Y_arr.append(point.y)
                    cv2.circle(hand_points_image, (X, Y), 1, (255, 255, 255), 3)
                hand_image_model = image

                draw.draw_landmarks(image, hand_landmarks, mp.solutions.hands.HAND_CONNECTIONS)

                try:
                    hand_image = cv2.resize(
                        image[int(min(Y_arr) * h): int(max(Y_arr) * h), int(min(X_arr) * w): int(max(X_arr) * w)],
                        dsize=(224, 224),
                        interpolation=cv2.INTER_AREA)
                except cv2.error:
                    pass

    return hand_points_image, hand_image, hand_image_model
