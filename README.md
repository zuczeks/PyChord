# PyChord
## Participants 
 - Izabela Bąk
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
- using machine-learning to teach the program to match chords correctly
- web application 


## PyChord Project Description

## Program User Interface

piano keyboard to enter the melody 
the staff with bars and notes displayed
additional buttons: key, number of bars and time measure choice, instrument choice (input is always the piano, but the output may be like guitar, flute, etc.), rhythm generation

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
playing on the piano

Sprint 2: (11.05 - 17.05)
staff visualisation with notes
notes letter names

Sprint 3: (18.05 - 24.05)
harmonizing the simple melody in fixed key
displaying chords

Sprint 4: (25.04 - 31.05)
instrument choice and output files
determining the key

Sprint 5: (1.06 - 7.06)
improvements of the piece (rhythm generation, more advanced harmonization)

Sprint 6: (8.06 - 14.06)
additionals 
final look
optional tests


## Basic harmonization algorithm
We have the key (chosen by user) and a bunch of notes (all the same measure) within this key (for example d minor). Another notes of the piano keyboard (which are not in given key) are disabled.
Next step is to recognize the set of basic chords in this key (d minor, g minor, A major, Bb major)
Then to group our notes into maximum groups that each note is contained in one chord from given above, and apply additional rules:
changing the chord on the “weak” part of the bar (meaning the 2nd and 4th measure in the 4/4 bar and 2nd and 3rd measure in the 3/4 bar) - the same chord may not last to the next bar
when maximum groups imply the chord change, we consider smaller groups and so on
We optionally end the melody with a keynote to make a nice ending.



## Some further improvements
Determining the key of the melody (which isn’t fixed), considering given notes, key characters and maybe the end note.
Generating the rhythm in order to have the notes in varying measures 





