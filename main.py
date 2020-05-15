from PyQt5.QtWidgets import QPushButton, QMainWindow, QApplication, QComboBox
import sys
from music21 import *
import subprocess
import platform
import os
from datetime import date
from Keyboard import Keyboard


class MyWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        
        self.stream1 = stream.Stream()
        self.stream1.insert(instrument.Piano())
        self.tmpStream = stream.Stream()
        self.tmpStream.insert(instrument.Piano())
        self.lpc = lily.translate.LilypondConverter()
        lp_music_list = lily.lilyObjects.LyMusicList()
        self.lpc.context = lp_music_list

        self.resize(1300, 700)
        self.setWindowTitle("PyChord")
        keyboard = Keyboard(self)
        play_button = QPushButton("Play", self)
        play_button.move(1100, 300)
        play_button.clicked.connect(self.play_notes)

        notes_button = QPushButton("Show Notes", self)
        notes_button.clicked.connect(self.show_notes)
        notes_button.move(1100, 350)

        save_button = QPushButton("Save", self)
        save_button.clicked.connect(self.save)
        save_button.move(1100, 400)

        cb = QComboBox(self)
        cb.move(1100, 250)
        cb.addItems(['Piano(default)', 'Guitar', 'Violin', 'Flute', 'Mandolin'])
        cb.currentIndexChanged.connect(self.change_instrument)

    def play_notes(self):
        sp = midi.realtime.StreamPlayer(self.stream1)
        sp.play()

    def show_notes(self):
        self.lpc.appendObjectsToContextFromStream(self.stream1)
        with open('try2.ly', 'w') as f:
            f.write('\\version "2.20.0"\n')
            f.write("{\n")
            f.write(str(self.lpc.context))
            f.write("}\n")

        if platform.system() == 'Linux':
            proc = subprocess.Popen(["lilypond try2.ly"], shell=True)
            proc.wait(100)

            subprocess.Popen(['chmod 755 try2.pdf'], shell=True)
            subprocess.Popen(['xdg-open try2.pdf'], shell=True)

        elif platform.system() == 'Windows':
            proc = subprocess.Popen(['powershell', 'lilypond try2.ly'])
            proc.wait(100)

            subprocess.Popen(['powershell', '.\\try2.pdf'])

    def save(self):
        if not os.path.exists('music'):
            os.makedirs('music')
        today = date.today()
        flag = True
        count = 1
        path = ''

        while flag is True:
            path = os.path.join('music', '{}.{}.mid'.format(str(count), str(today)))
            flag = os.path.isfile(path)
            count += 1

        self.stream1.write('midi', fp=path)

    def add_note(self, my_note):
        self.stream1.append(note.Note(my_note))
        self.tmpStream.append(note.Note(my_note))
        sp = midi.realtime.StreamPlayer(self.tmpStream)
        sp.play()
        self.tmpStream.pop(1)

    def change_instrument(self, choice):
        if choice == 0:
            self.stream1.insert(instrument.Piano())
        elif choice == 1:
            self.stream1.insert(instrument.AcousticGuitar())
        elif choice == 2:
            self.stream1.insert(instrument.Violin())
        elif choice == 3:
            self.stream1.insert(instrument.Flute())
        elif choice == 4:
            self.stream1.insert(instrument.Mandolin())


if __name__ == '__main__':
    app = QApplication([])
    app.setStyle('Fusion')
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())




