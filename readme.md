# Install required packages
!pip install mido


allow users to select available sequences and build a new MIDI

# MIDI Sequence Generator

This Python script generates MIDI sequences based on musical scales, arpeggios, and other patterns. It allows users to create MIDI files with custom sequences and repetitions.

## Features

- Generate sequences based on C Major and D Major scales.
- Create arpeggios from a given root note.
- Generate major triads arpeggio across all 12 semitones.
- Produce a circle of fifths arpeggio pattern.
- Create a fun piano piece by combining scales, arpeggios, and random runs.
- Repeat sequences for a specified number of times.
- Save the generated sequence as a MIDI file with a custom name.

## Requirements

- Python 3.x
- `mido` library for working with MIDI messages and files. Install it using `pip install mido`.

## Usage

1. Run the script using Python:
