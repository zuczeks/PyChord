from PyQt5.QtWidgets import QPushButton


class Keyboard:
    def __init__(self, window):
        self.buttons = []
        self.white_notes = ['F3', 'G3', 'A3', 'B3', 'C4', 'D4', 'E4', 'F4', 'G4',
                            'A4', 'B4', 'C5', 'D5', 'E5', 'F5', 'G5', 'A5', 'B5']
        self.black_notes = ['F#3', 'G#3', 'A#3', 'C#4', 'D#4', 'F#4', 'G#4', 'A#4', 'C#5', 'D#5', 'F#5', 'G#5', 'A#5']
        
        for i in range(0, 18):
            self.buttons.append(WhiteButton(window, self.white_notes[i]))
            self.buttons[i].move(40*i + 250, 450)

        arr = [0, 1, 2, 4, 5, 7, 8, 9, 11, 12, 14, 15, 16]

        for j, i in enumerate(arr):
            self.buttons.append(BlackButton(window, self.black_notes[j]))
            self.buttons[j+len(self.white_notes)].move(40*i + 278, 450)



class WhiteButton(QPushButton):
    def __init__(self, window, my_note):
        QPushButton.__init__(self, window)
        self.resize(40, 140)
        self.setStyleSheet("QPushButton {background-color: white}")
        self.clicked.connect(lambda: window.add_note(my_note))


class BlackButton(QPushButton):
    def __init__(self, window, my_note):
        QPushButton.__init__(self, window)
        self.resize(24, 90)
        self.clicked.connect(lambda: window.add_note(my_note))
        self.setStyleSheet("QPushButton {background-color: black} QPushButton:pressed {background-color: grey}")
