import cv2
import mediapipe as mp
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

zdjecia = [f'reka{x}.jpg' for x in range(1, 8)]

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
                palce = {
                    (1, "kciuk"): False,
                    (2, "wskazujacy"): False,
                    (3, "środkowy"): False,
                    (4, "serdeczny"): False,
                    (5, "mały"): False,
                }
                # rysowanie wykrych palców
                mp_drawing.draw_landmarks(
                    img,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style())
                # wyznaczenie ilosci palców
                lm_list = []
                id_punktow_koncowych = [4, 8, 12, 16, 20]
                id_punktow_poczatkowych = [2, 6, 10, 14, 17]

                for id, lm in enumerate(hand_landmarks.landmark):
                    wysokosc, szerokosc, c = img.shape
                    cx, cy = int(lm.x * szerokosc), int(lm.y * wysokosc)
                    lm_list.append([id, cx, cy])

                kotra_reka = ''
                # sprawdź czy to prawa albo lewa ręka
                # jesli x punktu 0 jest mniejsze od x punktu 1
                if lm_list[1][1] < lm_list[0][1]:
                    print('lewa')
                    kotra_reka = 'lewa'
                else:
                    print('prawa')
                    kotra_reka = 'prawa'

                for id, nazwa in palce:
                    if id == 1 and lm_list[id_punktow_koncowych[0]][1] > lm_list[id_punktow_poczatkowych[0]][1]:
                        palce[(id, nazwa)] = True
                    else:
                        if lm_list[id_punktow_koncowych[id-1]][2] < lm_list[id_punktow_poczatkowych[id-1]][2]:
                            palce[(id, nazwa)] = True

                # liczenie ilosci pokazanych palców
                ilosc_palcow = 0
                print(palce)
                for id, nazwa in palce:
                    if palce[id, nazwa]:
                        ilosc_palcow += 1

                print(f'Ilosc palcow: {ilosc_palcow}')

                # wyświatlanie liczby pokazywanych palców
                rec_size = (100, 180)
                cv2.rectangle(img, (img.shape[1], img.shape[0]), (img.shape[1]-rec_size[0], img.shape[0]-rec_size[1]),
                              (0, 0, 0), cv2.FILLED)
                cv2.putText(img, str(ilosc_palcow), (img.shape[1]-rec_size[0], img.shape[0]-40), cv2.FONT_HERSHEY_TRIPLEX,
                            5, (255, 255, 255), 20)

        cv2.imshow('MediaPipe Hands', img)
        cv2.waitKey(0)
