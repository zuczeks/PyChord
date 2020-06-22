from PyQt5.QtWidgets import QPushButton
from music21 import pitch


class Keyboard:
    def __init__(self, window):
        self.notes_count = 31
        self.pitches_in_order = []
        actual_pitch = pitch.Pitch('F-3')
        for i in range(0, self.notes_count):
            self.pitches_in_order.append(actual_pitch)
            actual_pitch.transpose(1)
            
        self.buttons = []
        self.buttons_in_order = []
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
        
    def set_buttons_in_order(self):
        black_counter = 0
        white_counter = 0
        for i in range(0, self.notes_count):
            if i in [1, 3, 5, 8, 10, 13, 15, 17, 21, 23, 26, 28, 30]:
                self.buttons_in_order.append(self.buttons[18 + black_counter])
                black_counter += 1
            else:
                self.buttons_in_order.append(self.buttons[white_counter])
                white_counter += 1
        
    def on_key_change(self, key):
        if key.mode == 'major':
            progression = [2, 2, 1, 2, 2, 2, 1]
        else:
            progression = [2, 1, 2, 2, 1, 2, 2]
        
        start = pitch.Pitch(key.tonic)
        notes_matching = []
        notes_matching_with_enharmonics = []
        notes_matching.append(start)
        for i, step in enumerate(progression):
            notes_matching.append(notes_matching[i].transpose(step))

        for note in notes_matching:
            notes_matching_with_enharmonics.append(note)
            for enharmonic in note.getAllCommonEnharmonics():
                notes_matching_with_enharmonics.append(enharmonic)

        for button in self.buttons:
            if button.common_pitch.name in [note.name for note in notes_matching_with_enharmonics]:
                button.setEnabled(True)
            else:
                button.setEnabled(False)
                button.setStyleSheet('QPushButton {background-color: lightgrey}')
    
    def reset(self):
        for button in self.buttons:
            button.setEnabled(True)
            if button.type == 'white':
                button.setStyleSheet('QPushButton {background-color: white}')
            else:
                button.setStyleSheet('QPushButton {background-color: black} '
                                     'QPushButton:pressed {background-color: grey}')


class WhiteButton(QPushButton):
    def __init__(self, window, my_note):
        QPushButton.__init__(self, window)
        self.resize(40, 140)
        self.setStyleSheet('QPushButton {background-color: white}')
        self.common_name = my_note
        self.common_pitch = pitch.Pitch(my_note)
        self.pitches = self.common_pitch.getAllCommonEnharmonics()
        self.type = 'white'
        self.clicked.connect(lambda: window.add_note(self.common_pitch))
        

class BlackButton(QPushButton):
    def __init__(self, window, my_note):
        QPushButton.__init__(self, window)
        self.resize(24, 90)
        self.setStyleSheet('QPushButton {background-color: black} QPushButton:pressed {background-color: grey}')
        self.common_name = my_note
        self.common_pitch = pitch.Pitch(my_note)
        self.pitches = self.common_pitch.getAllCommonEnharmonics()
        self.type = 'black'
        self.clicked.connect(lambda: window.add_note(self.common_pitch))
