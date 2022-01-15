import cv2
import mediapipe as mp
from liczeniePalcow import liczeniePalcow

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

cap = cv2.VideoCapture(0)
with mp_hands.Hands(
        model_complexity=0,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as hands:
    while cap.isOpened():

        success, image = cap.read()

        if not success:
            print("Ignoring empty camera frame.")
            continue

        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = hands.process(image)

        # Draw the hand annotations on the image.
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    image,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style())

            reka = liczeniePalcow(hand_landmarks, image)
            # reka.wypisz_status()
            ilosc_palcow = reka.iloscPalcow()
            rec_size = (100, 180)
            cv2.rectangle(image, (image.shape[1], image.shape[0]), (image.shape[1]-rec_size[0], image.shape[0]-rec_size[1]),
                          (0, 0, 0), cv2.FILLED)
            cv2.putText(image, reka.orientacja, (
                image.shape[1]-rec_size[0], image.shape[0]), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 1)
            cv2.putText(image, str(ilosc_palcow), (image.shape[1]-rec_size[0], image.shape[0]-40), cv2.FONT_HERSHEY_TRIPLEX,
                        5, (255, 255, 255), 20)

        cv2.imshow('MediaPipe Hands', image)

        if cv2.waitKey(5) & 0xFF == 27:
            break

cap.release()
