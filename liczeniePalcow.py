class liczeniePalcow:
    def __init__(self, hand_landmarks, img):
        self.hand_landmarks = hand_landmarks
        self.img = img
        self.palce = {
            (1, "kciuk"): False,
            (2, "wskazujacy"): False,
            (3, "środkowy"): False,
            (4, "serdeczny"): False,
            (5, "mały"): False,
        }
        self.id_punktow = {
            'koncowych': [3, 8, 12, 16, 20],
            'poczatkowych': [5, 6, 10, 14, 17]
        }
        self.__liczeniePalcow()
        self.orientacja = self.__orientacjaDloni()
        self.__sprawdzPalce()

    def __liczeniePalcow(self):
        self.lista_lm = []
        for id, lm in enumerate(self.hand_landmarks.landmark):
            wysokosc, szerokosc, c = self.img.shape
            cx, cy = int(lm.x * szerokosc), int(lm.y * wysokosc)
            self.lista_lm.append([id, cx, cy])
        return self.lista_lm

    def __orientacjaDloni(self):
        # sprawdź czy to prawa albo lewa ręka
        # jesli x punktu 0 jest większe od x punktu 1
        if self.lista_lm[0][1] > self.lista_lm[1][1]:
            return 'lewa'
        else:
            return 'prawa'

    def __sprawdzPalce(self):
        for id, nazwa in self.palce:
            k = self.id_punktow['koncowych'][id-1]
            p = self.id_punktow['poczatkowych'][id-1]
            # dla kciuka  lm[id,x,y]
            if id == 1:
                if self.orientacja == 'lewa':
                    if self.lista_lm[k][1] < self.lista_lm[p][1]:
                        self.palce[id, nazwa] = True
                else:
                    if self.lista_lm[k][1] > self.lista_lm[p][1]:
                        self.palce[id, nazwa] = True
            else:
                if self.lista_lm[k][2] < self.lista_lm[p][2]:
                    self.palce[(id, nazwa)] = True

    def wypisz_status(self):
        print(10*'-')
        print(f'Orientacja dloni: {self.orientacja}')
        for i, p in self.palce:
            print(f'{p} {self.palce[(i,p)]}')
        print(10*'-')

    def iloscPalcow(self):
        # liczenie ilosci pokazanych palców
        self.ilosc_palcow = 0
        for id, nazwa in self.palce:
            if self.palce[id, nazwa]:
                self.ilosc_palcow += 1

        return self.ilosc_palcow
