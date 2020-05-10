from PyQt5.QtWidgets import QPushButton, QMainWindow, QApplication
import sys
from music21 import *
import subprocess
import platform
import os
from datetime import date


stream1 = stream.Stream()
stream1.insert(instrument.Piano())
tmpStream = stream.Stream()
tmpStream.insert(instrument.Piano())
lpc = lily.translate.LilypondConverter()
lpMusicList = lily.lilyObjects.LyMusicList()
lpc.context = lpMusicList


def play_notes():
    sp = midi.realtime.StreamPlayer(stream1)
    sp.play()


def show_notes():
    lpc.appendObjectsToContextFromStream(stream1)
    with open('try2.ly', 'w') as f:
        f.write('\\version "2.20.0"\n')
        f.write("{\n")
        f.write(str(lpc.context))
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


def save():
    if not os.path.exists('music'):
        os.makedirs('music')
    today = date.today()
    flag = True
    count = 1

    while flag is True:
        path = os.path.join('music', '{}.{}.mid'.format(str(count), str(today)))
        flag = os.path.isfile(path)
        count += 1

    stream1.write('midi', fp=path)


def add_note(my_note):
    stream1.append(note.Note(my_note))
    tmpStream.append(note.Note(my_note))
    sp = midi.realtime.StreamPlayer(tmpStream)
    sp.play()
    tmpStream.pop(1)


def my_window():
    app = QApplication([])
    app.setStyle('Fusion')
    window = QMainWindow()
    window.resize(1300, 700)
    window.setWindowTitle("PyChord")
    keyboard(window)
    play_button = QPushButton("Play", window)
    play_button.move(1100, 300)
    play_button.clicked.connect(play_notes)

    notes_button = QPushButton("Show Notes", window)
    notes_button.clicked.connect(show_notes)
    notes_button.move(1100, 350)

    save_button = QPushButton("Save", window)
    save_button.clicked.connect(save)
    save_button.move(1100, 400)

    window.show()
    sys.exit(app.exec_())


def keyboard(window):
    buttons = []
    white_notes = ['F3', 'G3', 'A3', 'B3', 'C4', 'D4', 'E4', 'F4', 'G4',
                   'A4', 'B4', 'C5', 'D5', 'E5', 'F5', 'G5', 'A5', 'B5']
    black_notes = ['F#3', 'G#3', 'A#3', 'C#4', 'D#4', 'F#4', 'G#4', 'A#4', 'C#5', 'D#5', 'F#5', 'G#5', 'A#5']
    for i in range(0, 18):
        buttons.append(white_button(window, 40*i + 250, 450, white_notes[i]))

    arr = [0, 1, 2, 4, 5, 7, 8, 9, 11, 12, 14, 15, 16]
    j = 0
    for i in arr:
        buttons.append(black_button(window, 40*i + 278, 450, black_notes[j]))
        j += 1


def white_button(window, x, y, my_note):
    button = QPushButton(window)
    button.resize(40, 140)
    button.clicked.connect(lambda: add_note(my_note))
    button.move(x, y)
    return button


def black_button(window, x, y, my_note):
    button = QPushButton(window)
    button.resize(24, 90)
    button.move(x, y)
    button.clicked.connect(lambda: add_note(my_note))
    button.setStyleSheet("QPushButton {background-color: black} QPushButton:pressed {background-color: grey}")

    return button


if __name__ == '__main__':
    my_window()



