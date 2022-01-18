import cv2
import mediapipe as mp
from liczeniePalcow import liczeniePalcow

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

zdjecia = [f'reka{x}.jpg' for x in range(1, 6)]

with mp_hands.Hands(
        static_image_mode=True,
        model_complexity=0,
        min_detection_confidence=0.5) as hands:

    for zdjecie in zdjecia:
        img = cv2.imread(zdjecie)
        img = cv2.cvtColor(cv2.flip(img, 1), cv2.COLOR_BGR2RGB)
        results = hands.process(img)
        # narysowanie wykrytych palców
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # rysowanie wykrych palców
                mp_drawing.draw_landmarks(
                    img,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style())

                reka = liczeniePalcow(hand_landmarks, img)
                reka.wypisz_status()
                ilosc_palcow = reka.iloscPalcow()

                # wyświatlanie liczby pokazywanych palców
                rec_size = (100, 180)
                cv2.rectangle(img, (img.shape[1], img.shape[0]), (img.shape[1]-rec_size[0], img.shape[0]-rec_size[1]),
                              (0, 0, 0), cv2.FILLED)
                cv2.putText(img, reka.orientacja, (
                    img.shape[1]-rec_size[0], img.shape[0]), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 1)
                cv2.putText(img, str(ilosc_palcow), (img.shape[1]-rec_size[0], img.shape[0]-40), cv2.FONT_HERSHEY_TRIPLEX,
                            5, (255, 255, 255), 20)

        cv2.imshow('MediaPipe Hands', img)
        cv2.waitKey(0)
