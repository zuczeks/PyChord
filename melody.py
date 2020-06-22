import copy
from PyQt5.QtWidgets import QPushButton
from music21 import pitch, chord, stream, meter


class Melody:
    def __init__(self, window, actual_key):
        self.note_buttons = []
        self.rhythmic_values_sum = 0
        self.notes_counter = 0
        self.actual_meter = 4
        self.actual_key = actual_key
        self.max_notes = 4 * self.actual_meter
        self.is_well_rhythmic = True
        self.window = window
        self.list_of_chords = []

    def show_melody(self):
        position = 0
        self.is_well_rhythmic = True
        for i in range(len(self.note_buttons)):
            mod_before = position % self.actual_meter
            mod_after = (position + self.note_buttons[i].rhythmic_value) % self.actual_meter

            if not (mod_after > mod_before or mod_after == 0):
                self.is_well_rhythmic = False
                integer = int(position / self.actual_meter)
                position = (integer + 1) * self.actual_meter

            self.note_buttons[i].resize(45 * self.note_buttons[i].rhythmic_value, 45)
            self.note_buttons[i].move(250 + position * 45, 300)
            self.note_buttons[i].show()
            position += self.note_buttons[i].rhythmic_value

    def add_note_to_melody(self, my_note):
        bar = 0
        self.rhythmic_values_sum = sum(self.note_buttons[i].rhythmic_value for i in range(len(self.note_buttons)))
        if self.rhythmic_values_sum < self.max_notes:
            self.note_buttons.append(MyNote(self.window, my_note.nameWithOctave))
            if self.max_notes - self.rhythmic_values_sum == 0.5:
                self.note_buttons[self.notes_counter].rhythmic_value = 0.5
            if self.notes_counter % 4 == 0:
                bar += 1
            self.notes_counter += 1

    def add_rhythm_to_melody(self, note):
        index = self.note_buttons.index(note)
        self.note_buttons[index].add_rhythm(self.actual_meter)
        self.rhythmic_values_sum = sum(self.note_buttons[i].rhythmic_value for i in range(len(self.note_buttons)))
        while self.rhythmic_values_sum > self.max_notes:
            self.note_buttons[index].add_rhythm(self.actual_meter)
            self.rhythmic_values_sum = sum(self.note_buttons[i].rhythmic_value for i in range(len(self.note_buttons)))

        for i in range(index + 1, len(self.note_buttons)):
            tmp = sum(self.note_buttons[j].rhythmic_value for j in range(i))
            self.window.melody_stream[i + 2].offset = tmp + 2

        self.window.melody_stream[index + 2].duration.quarterLength = self.note_buttons[index].rhythmic_value
        self.show_melody()

    def on_meter_change(self, new_meter):
        self.actual_meter = new_meter
        self.max_notes = 4 * self.actual_meter

    @staticmethod
    def normalize(current_pitch):
        if current_pitch.accidental == pitch.Pitch(accidental='-').accidental:
            return current_pitch.getEnharmonic()
        else:
            return current_pitch

    def functions(self):
        if self.actual_key is not None:
            start = pitch.Pitch(self.actual_key.tonic.name)
            start.octave = 2
            tonic = chord.Chord([start,
                                 pitch.Pitch(self.normalize(start.transpose(12))),
                                 pitch.Pitch(self.normalize(start.transpose(16))),
                                 pitch.Pitch(self.normalize(start.transpose(19)))])
            subdominant = chord.Chord([pitch.Pitch(self.normalize(start.transpose(5))),
                                       pitch.Pitch(self.normalize(start.transpose(12))),
                                       pitch.Pitch(self.normalize(start.transpose(17))),
                                       pitch.Pitch(self.normalize(start.transpose(21)))])
            dominant = chord.Chord([pitch.Pitch(self.normalize(start.transpose(7))),
                                    pitch.Pitch(self.normalize(start.transpose(11))),
                                    pitch.Pitch(self.normalize(start.transpose(14))),
                                    pitch.Pitch(self.normalize(start.transpose(19)))])

            result = [tonic, subdominant, dominant]
            return result

    def harmonize(self):
        [tonic, subdominant, dominant] = self.functions()
        self.list_of_chords = []
        first_note = self.window.melody_stream[2]
        if first_note.name in tonic.pitchNames:
            chord = tonic
        elif first_note.name in subdominant.pitchNames:
            chord = subdominant
        else:
            chord = dominant

        stream2 = stream.Stream()
        stream2.insert(0, self.window.actual_instrument)
        stream2.insert(1, meter.TimeSignature('{}/4'.format(self.window.actual_meter)))

        offset = self.window.melody_stream[2].offset
        chord.duration.quarterLength = 0
        for note in self.window.melody_stream[2:]:
            stream2.insert(note.offset, note)

            if note.name in chord.pitchNames:
                chord.duration.quarterLength += note.duration.quarterLength
            else:
                stream2.insert(offset, copy.deepcopy(chord))

                tmp_chords = []
                if note.name in tonic.pitchNames:
                    tmp_chords.append(tonic)
                if note.name in subdominant.pitchNames:
                    tmp_chords.append(subdominant)
                if note.name in dominant.pitchNames:
                    tmp_chords.append(dominant)
                if len(tmp_chords) == 1:
                    chord = tmp_chords[0]
                else:
                    if chord == dominant:
                        chord = tonic
                    else:
                        chord = dominant
                chord.duration.quarterLength = note.duration.quarterLength
                offset = note.offset

            self.list_of_chords.append(str(self.make_chord_name_to_lilypond(chord.pitchNames[0])) + str(
                int(4/note.duration.quarterLength)))

        chords_compression = []
        prev = self.list_of_chords[0]
        flag = 0
        for i, act in enumerate(self.list_of_chords[1:]):
            if flag == 1:
                prev = act
                flag = 0
                if i == len(self.list_of_chords) - 2:
                    chords_compression.append(prev)
            elif act[0] != prev[0]:
                chords_compression.append(prev)
                prev = act
                if i == len(self.list_of_chords) - 2:
                    chords_compression.append(prev)
            else:
                temp = list(act)
                length = int(prev[-1]) + int(act[-1])
                if length == 3:
                    temp[-1] = "1."
                    chords_compression.append("".join(map(str, temp)))
                elif length == 4:
                    temp[-1] = "1"
                    chords_compression.append("".join(map(str, temp)))
                elif length == 6:
                    temp[-1] = "2."
                    chords_compression.append("".join(map(str, temp)))
                elif length == 8:
                    temp[-1] = "2"
                    chords_compression.append("".join(map(str, temp)))
                elif length == 12:
                    temp[-1] = "4."
                    chords_compression.append("".join(map(str, temp)))
                elif length == 16:
                    temp[-1] = "4"
                    chords_compression.append("".join(map(str, temp)))
                else:
                    chords_compression.append(act)
                flag = 1

        self.list_of_chords = chords_compression
        stream2.insert(offset, copy.deepcopy(chord))
        self.window.harmonized_melody_stream = stream2

    @staticmethod
    def make_chord_name_to_lilypond(pitch_name):
        if len(pitch_name) == 1:
            return pitch_name
        else:
            if pitch_name[1] == '#':
                return str(pitch_name[0] + "is")


class MyNote(QPushButton):
    def __init__(self, window, my_note):
        QPushButton.__init__(self, window)
        self.resize(45, 45)
        self.setEnabled(True)
        self.rhythmic_value = 1
        self.setText(my_note)
        self.clicked.connect(lambda: window.melody.add_rhythm_to_melody(self))

    def add_rhythm(self, actual_meter):
        if self.rhythmic_value == 4:
            self.rhythmic_value = 0.5
        else:
            self.rhythmic_value *= 2

        if self.rhythmic_value > actual_meter:
            self.add_rhythm(actual_meter)
