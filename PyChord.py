from PyQt5.QtWidgets import QPushButton, QMainWindow, QApplication, QComboBox, QLabel, QMessageBox, QSlider, QLCDNumber
from PyQt5.QtGui import QPainter, QPen, QColor
from PyQt5.QtCore import Qt
import sys
from music21 import instrument, stream, lily, note, meter, key, exceptions21
import subprocess
import platform
import os
from datetime import date
from melody import Melody
from Keyboard import Keyboard
from pygame import mixer


class MyWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.resize(1300, 700)
        self.setFixedSize(self.size())
        self.setWindowTitle('PyChord')
        self.add_combo_boxes()
        self.add_buttons()
        self.sl = QSlider(Qt.Horizontal, self)
        self.volume = QLCDNumber(self)
        self.add_slider()

        self.actual_key = None
        self.actual_meter = 4
        self.actual_instrument = instrument.Piano()
        self.melody_stream = stream.Stream()
        self.harmonized_melody_stream = stream.Stream()
        self.reset_stream(self.melody_stream)
        self.reset_stream(self.harmonized_melody_stream)
        mixer.init(44100, -16, 2, 1024)

        self.tmpStream = stream.Stream()
        self.tmpStream.insert(instrument.Piano())
        self.lpc = lily.translate.LilypondConverter()
        self.lpc.context = lily.lilyObjects.LyMusicList()
        self.keyboard = Keyboard(self)
        self.melody = Melody(self, self.actual_key)

    def change_volume(self, vl):
        mixer.music.set_volume(vl / 100.0)
        self.volume.display(vl)

    def add_buttons(self):
        play_button = QPushButton('Play', self)
        play_button.move(1100, 300)
        play_button.clicked.connect(self.play_notes)

        reset_button = QPushButton('Reset', self)
        reset_button.move(1100, 350)
        reset_button.clicked.connect(self.reset)

        notes_button = QPushButton('Show Notes', self)
        notes_button.clicked.connect(self.show_notes)
        notes_button.move(1100, 400)

        save_button = QPushButton('Save', self)
        save_button.clicked.connect(self.save)
        save_button.move(1100, 450)

    def add_combo_boxes(self):
        key_info = QLabel('Choose a key:', self)
        key_info.move(600, 50)
        key_choice = QComboBox(self)
        key_choice.move(600, 100)
        key_choice.addItems(['None', 'C', 'D', 'E', 'F', 'G', 'A', 'B'])
        key_choice.currentIndexChanged.connect(self.change_key)

        meter_info = QLabel('Choose a meter:', self);
        meter_info.move(400, 50)
        meter_choice = QComboBox(self)
        meter_choice.move(400, 100)
        meter_choice.addItems(['4/4', '3/4', '2/4'])
        meter_choice.currentIndexChanged.connect(self.change_meter)

        instrument_choice = QComboBox(self)
        instrument_choice.move(1100, 250)
        instrument_choice.addItems(['Piano(default)', 'Guitar', 'Violin', 'Flute', 'Mandolin'])
        instrument_choice.currentIndexChanged.connect(self.change_instrument)

    def add_slider(self):
        self.sl.setMinimum(0)
        self.sl.setMaximum(100)
        self.sl.setValue(80)
        self.sl.setTickInterval(1)
        self.sl.move(1100, 220)
        self.sl.valueChanged.connect(lambda: self.change_volume(self.sl.value()))

        self.volume.move(1100, 180)
        self.volume.display(80)

    def play_notes(self):
        try:
            if not self.melody.is_well_rhythmic:
                confirm = QMessageBox()
                confirm.setWindowTitle('Error')
                confirm.setText('The rhythm is not correct.')
                confirm.setIcon(QMessageBox.Information)
                confirm.exec()
            else:
                if self.actual_key is not None:
                    self.melody.harmonize()
                    mixer.music.load(self.harmonized_melody_stream.write('midi'))
                    mixer.music.play()
                else:
                    mixer.music.load(self.melody_stream.write('midi'))
                    mixer.music.play()
        except exceptions21.StreamException:
            pass

    def show_notes(self):
        if not self.melody.is_well_rhythmic:
            confirm = QMessageBox()
            confirm.setWindowTitle('Error')
            confirm.setText('The rhythm is not correct.')
            confirm.setIcon(QMessageBox.Information)
            confirm.exec()
        else:
            self.lpc.context.contents = []
            self.lpc.appendObjectsToContextFromStream(self.melody_stream)

            with open('notes.ly', 'w+') as f:
                f.write('\\version "2.20.0"\n')
                if self.actual_key is None:
                    f.write("{\n")
                    f.write('\\key c \\major \n')
                    f.write(str(self.lpc.context))
                    f.write("}\n")
                else:
                    f.write('{<<\n')
                    f.write('\\chords {')
                    for i in self.melody.list_of_chords:
                        f.write(i.lower() + " ")
                    f.write('}\n')
                    f.write('{\\key ' + self.actual_key.tonic.name.lower() + ' \\' + self.actual_key.mode)
                    f.write('\n')
                    f.write(str(self.lpc.context))
                    f.write('}>>}\n')

            if platform.system() == 'Linux':
                process = subprocess.Popen(['lilypond notes.ly'], shell=True)
                process.wait(100)

                subprocess.Popen(['chmod 755 notes.pdf'], shell=True)
                subprocess.Popen(['xdg-open notes.pdf'], shell=True)

            elif platform.system() == 'Windows':
                process = subprocess.Popen(['powershell', 'lilypond notes.ly'])
                process.wait(100)

                subprocess.Popen(['powershell', '.\\notes.pdf'])

    def save(self):
        if not self.melody.is_well_rhythmic:
            confirm = QMessageBox()
            confirm.setWindowTitle('Error')
            confirm.setText('The rhythm is not correct.')
            confirm.setIcon(QMessageBox.Information)
            confirm.exec()
        else:
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

            self.harmonized_melody_stream.write('midi', fp=path)
            confirm = QMessageBox()
            confirm.setWindowTitle('Confirmation')
            confirm.setText('File saved')
            confirm.setIcon(QMessageBox.Information)
            confirm.exec()

    def add_note(self, my_note):
        self.melody.rhythmic_values_sum = sum(
            self.melody.note_buttons[i].rhythmic_value for i in range(len(self.melody.note_buttons)))
        if self.melody.rhythmic_values_sum < self.melody.max_notes:
            self.melody_stream.insert(self.melody.rhythmic_values_sum + 2, note.Note(my_note.nameWithOctave))
            for i in range(8):
                if mixer.Channel(i).get_busy():
                    pass
                else:
                    if platform.system() == 'Linux':
                        mixer.Channel(i).play(mixer.Sound('notes/{}.wav'.format(my_note)))
                    elif platform.system() == 'Windows':
                        mixer.Channel(i).play(mixer.Sound('notes\\{}.wav'.format(my_note)))
                    break
            self.melody.add_note_to_melody(my_note)
            self.melody.show_melody()

    def reset_stream(self, stream_to_reset):
        stream_to_reset.clear()
        stream_to_reset.insert(0, self.actual_instrument)
        stream_to_reset.insert(1, meter.TimeSignature('{}/4'.format(self.actual_meter)))

    def change_instrument(self, choice):
        instruments = [instrument.Piano(), instrument.AcousticGuitar(), instrument.Violin(), instrument.Flute(),
                       instrument.Mandolin()]
        self.actual_instrument = instruments[choice]
        self.melody_stream[0] = self.actual_instrument

    def reset(self):
        for button in self.melody.note_buttons:
            button.hide()
        self.melody.note_buttons.clear()
        self.melody.notes_counter = 0
        self.melody.rhythmic_values_sum = 0
        self.reset_stream(self.melody_stream)
        self.reset_stream(self.harmonized_melody_stream)

    def change_key(self, choice):
        self.reset()
        self.keyboard.reset()
        if choice == 0:
            self.actual_key = None
        else:
            keys = ['None', 'C', 'D', 'E', 'F', 'G', 'A', 'B']
            self.actual_key = key.Key(keys[choice])
            self.keyboard.on_key_change(self.actual_key)

        self.melody.actual_key = self.actual_key

    def change_meter(self, choice):
        self.reset()
        meters = [4, 3, 2]
        self.actual_meter = meters[choice]
        self.melody.on_meter_change(self.actual_meter)
        self.update(0, 0, 1000, 1000)

    def paintEvent(self, e):
        lines = QPainter(self)
        lines.setPen(QPen(QColor(240, 240, 240), 10, Qt.SolidLine))
        for i in range(17):
            lines.drawLine(250 + i * 45, 290, 250 + i * 45, 350)

        lines.setPen(QPen(Qt.black, 10, Qt.SolidLine))
        for i in range(5):
            lines.drawLine(250 + i * self.actual_meter * 45, 290, 250 + i * self.actual_meter * 45, 350)
        lines.end()


if __name__ == '__main__':
    app = QApplication([])
    app.setStyle('Fusion')
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
