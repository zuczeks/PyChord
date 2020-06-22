
# PyChord
## Participants 
 - Izabela Bąk - teamleader
 - Wiktor Jasiński
 - Adrianna Pytel
 - Szymon Telega
### Do you need more people: Maybe
## Short description of the idea
The main issue of the project is to harmonize and rhythmize given melodic line, using machine learning. The user may expext a little own-composed music piece based on their own melody, with added rhythm and full chords (harmonic sets of pitches consisting of multiple notes, heard simultaneously) that match all these.

## Features:
- nice user interface that allows the user to put in their own melody like the piano 
- radomization of nice, logical and natural rhythm to be a basis for chords creation
- output in the form of audible music piece and guitar/piano chords
- optionally using machine-learning to teach the program to match chords correctly

## Instalation:
To run PyChord you need to follow this steps:
- regardless of the OS you're using, install Lilipond: http://lilypond.org/download.html. To run the code on Windows it is necessary also to add the LilyPond\usr\bin folder to path.
- on linux you'll also need some synthesizer that can play MIDI files (i.e. Timidity)
- install packages from requirements.txt - run 'pip install -r requirements.txt'
- run application with 'python PyChord.py'


## PyChord Project Description

### Program tutorial in polish
https://drive.google.com/file/d/1zzrpaT-NJmUdgPgN3l2LFZcjD1JjpV2r/view?usp=sharing

## Program User Interface

- piano keyboard to enter the melody 
- the staff with bars and notes displayed
- additional buttons: key, number of bars and time measure choice, instrument choice (input is always the piano, but the output may be like guitar, flute, etc.), rhythm generation

## Functions to implement

-  playing tones chosen from the screen piano keyboard
-  displaying notes on the staff
-  displaying notes' letter names
-  entering notes directly on the staff
-  creating and playing triads in given key
-  harmonizing the simple melody in fixed length and key
-  determining the key of given melody
-  harmonizing given melody without fixed key
-  generating the rhythm to the melody
-  harmonizing the piece (melody + rhythm)
-  displaying generated chords 
-  possibility to choose instrument played
-  saving generated piece (midi file or else)

## Working on project

Sprint 1: (4.05 - 10.05)
GUI basics
- playing on the piano

Sprint 2: (11.05 - 17.05)
- staff visualisation with notes
- notes letter names

Sprint 3: (18.05 - 24.05)
- harmonizing the simple melody in fixed key
- displaying chords

Sprint 4: (25.04 - 31.05)
- instrument choice and output files
- determining the key

Sprint 5: (1.06 - 7.06)
- improvements of the piece (rhythm generation, more advanced harmonization)

Sprint 6: (8.06 - 14.06)
- additionals 
- final look
- optional tests


## Basic harmonization algorithm
https://docs.google.com/document/d/1O2371Rh-Jzn-JSPzkmYcQ7uEdMk8movFK-UW56fM7iY/edit?usp=sharing



## Some further improvements
- Determining the key of the melody (which isn’t fixed), considering given notes, key characters and maybe the end note.
- Generating the rhythm in order to have the notes in varying measures 






