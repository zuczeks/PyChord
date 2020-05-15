from PyQt5.QtWidgets import QPushButton, QMainWindow, QApplication, QComboBox, QMessageBox, QSlider, QLCDNumber
from PyQt5.QtCore import Qt
import sys
from music21 import *
from PyQt5 import QtGui
import subprocess
import platform
import os
from datetime import date
from Keyboard import Keyboard
from pygame import mixer


class MyWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MyWindow, self).__init__(parent)

        self.stream1 = stream.Stream()
        self.stream1.insert(instrument.Piano())
        self.tmpStream = stream.Stream()
        self.tmpStream.insert(instrument.Piano())
        self.lpc = lily.translate.LilypondConverter()
        lp_music_list = lily.lilyObjects.LyMusicList()
        self.lpc.context = lp_music_list
        mixer.init(44100, -16, 2, 1024)
        mixer.music.set_volume(0.8)
        self.resize(1300, 700)
        self.setWindowTitle("PyChord")
        path = os.path.join('images', 'icon.png')
        self.setWindowIcon(QtGui.QIcon(path))

        Keyboard(self)
        self.play_button = QPushButton("Play", self)
        self.play_button.move(1100, 300)
        self.play_button.clicked.connect(self.play_notes)

        self.notes_button = QPushButton("Show Notes", self)
        self.notes_button.clicked.connect(self.show_notes)
        self.notes_button.move(1100, 350)

        self.save_button = QPushButton("Save", self)
        self.save_button.clicked.connect(self.save)
        self.save_button.move(1100, 400)

        self.sl = QSlider(Qt.Horizontal, self)
        self.sl.setMinimum(0)
        self.sl.setMaximum(100)
        self.sl.setValue(80)
        self.sl.setTickInterval(1)
        self.sl.move(1100, 250)
        self.sl.valueChanged.connect(lambda: self.change_volume(self.sl.value()))

        self.volume = QLCDNumber(self)
        self.volume.move(1100, 220)
        self.volume.display(80)

        cb = QComboBox(self)
        cb.move(1100, 190)
        cb.addItems(['Piano(default)', 'Guitar', 'Violin', 'Flute', 'Mandolin'])
        cb.currentIndexChanged.connect(self.change_instrument)

    def change_volume(self, vl):
        mixer.music.set_volume(vl/100.0)
        self.volume.display(vl)

    def play_notes(self):
        mixer.music.load(self.stream1.write('midi'))
        mixer.music.play()

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
        confirm = QMessageBox()
        confirm.setWindowTitle("Confirmation")
        confirm.setText("File saved")
        confirm.setIcon(QMessageBox.Information)
        confirm.exec()

    def add_note(self, my_note):
        self.stream1.append(note.Note(my_note))
        self.tmpStream.append(note.Note(my_note))
        mixer.music.load(self.tmpStream.write('midi'))
        mixer.music.play()
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

# # genPlayM21Score.py Generates and Plays 2 Music21 Scores "on the fly".
# #
# # see way below for source notes
#
# from music21 import *
#
# # we create the music21 Bottom Part, and do this explicitly, one object at a time.
#
# n1 = note.Note('e4')
# n1.duration.type = 'whole'
# n2 = note.Note('d4')
# n2.duration.type = 'whole'
# m1 = stream.Measure()
# m2 = stream.Measure()
# m1.append(n1)
# m2.append(n2)
# partLower = stream.Part()
# partLower.append(m1)
# partLower.append(m2)
#
# # For the music21 Upper Part, we automate the note creation procedure
#
# data1 = [('g4', 'quarter'), ('a4', 'quarter'), ('b4', 'quarter'), ('c#5', 'quarter')]
# data2 = [('d5', 'whole')]
# data = [data1, data2]
# partUpper = stream.Part()
#
# def makeUpperPart(data):
#     for mData in data:
#         m = stream.Measure()
#         for pitchName, durType in mData:
#             n = note.Note(pitchName)
#             n.duration.type = durType
#             m.append(n)
#         partUpper.append(m)
# makeUpperPart(data)
#
# # Now, we can add both Part objects into a music21 Score object.
#
# sCadence = stream.Score()
# sCadence.insert(0, partUpper)
# sCadence.insert(0, partLower)
#
# # Now, let's play the MIDI of the sCadence Score
# # [from memory, ie no file  write necessary] using pygame
#
# import cStringIO
#
# sCadence_mf = sCadence.midiFile
# sCadence_mStr = sCadence_mf.writestr()
# sCadence_mStrFile = cStringIO.StringIO(sCadence_mStr)
#
# import pygame
#
# freq = 44100    # audio CD quality
# bitsize = -16   # unsigned 16 bit
# channels = 2    # 1 is mono, 2 is stereo
# buffer = 1024    # number of samples
# pygame.mixer.init(freq, bitsize, channels, buffer)
#
# # optional volume 0 to 1.0
# pygame.mixer.music.set_volume(0.8)
#
# def play_music(music_file):
#     """
#     stream music with mixer.music module in blocking manner
#     this will stream the sound from disk while playing
#     """
#     clock = pygame.time.Clock()
#     try:
#         pygame.mixer.music.load(music_file)
#         print "Music file %s loaded!" % music_file
#     except pygame.error:
#         print "File %s not found! (%s)" % (music_file, pygame.get_error())
#         return
#     pygame.mixer.music.play()
#     while pygame.mixer.music.get_busy():
#         # check if playback has finished
#         clock.tick(30)
#
# # play the midi file we just saved
# play_music(sCadence_mStrFile)
#
# #============================
#
# # now let's make a new music21 Score by reversing the upperPart notes
# data1.reverse()
# data2 = [('d5', 'whole')]
# data = [data1, data2]
# partUpper = stream.Part()
# makeUpperPart(data)
# sCadence2 = stream.Score()
# sCadence2.insert(0, partUpper)
# sCadence2.insert(0, partLower)
#
# # now let's play the new Score
# sCadence2_mf = sCadence2.midiFile
# sCadence2_mStr = sCadence2_mf.writestr()
# sCadence2_mStrFile = cStringIO.StringIO(sCadence2_mStr)
# play_music(sCadence2_mStrFile)




