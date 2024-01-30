import random
import mido
from mido import MidiFile, MidiTrack, Message

# Define a sequence: (note, velocity, ticks)
# Define a sequence: (note, velocity, ticks)
C_Major = [
    (60, 64, 480),  # Note C4, quarter note
    (62, 64, 480),  # Note D4, quarter note
    (64, 64, 480),  # Note E4, quarter note
    (65, 64, 480),  # Note F4, quarter note
   (67, 64, 480),  # Note G4, quarter note
   (69, 64, 480),  # Note A4, quarter note
   (71, 64, 480),  # Note B4, quarter note
   (72, 64, 480),  # Note C5, quarter note
]

# Define a D Major scale sequence: (note, velocity, ticks)
D_Major = [
    (62, 64, 480),  # Note D4, quarter note
    (64, 64, 480),  # Note E4, quarter note
    (66, 64, 480),  # Note F#4, quarter note
    (67, 64, 480),  # Note G4, quarter note
    (69, 64, 480),  # Note A4, quarter note
    (71, 64, 480),  # Note B4, quarter note
    (73, 64, 480),  # Note C#5, quarter note
    (74, 64, 480),  # Note D5, quarter note
]


AR1 = [
    (60, 64, 480),  # Note C4, quarter note
    (64, 64, 480),  # Note E4, quarter note
    (67, 64, 480),  # Note G4, quarter note
    (72, 64, 960),  # Note C5, half note
    (67, 64, 480),  # Note G4, quarter note
    (64, 64, 480),  # Note E4, quarter note
    (60, 64, 960),  # Note C4, half note
]

# Create a dictionary to map user options to the scale sequences
scale_sequences = {
    '1': C_Major,
    '2': D_Major,
    'AR1': AR1,
}

# Add an option for generating a major scale based on a root note



def generate_major_scale(root_note):
    # Major scale intervals: whole, whole, half, whole, whole, whole, half
    intervals = [2, 2, 1, 2, 2, 2, 1]
    scale = [(root_note, 64, 480)]
    for interval in intervals:
        root_note += interval
        scale.append((root_note, 64, 480))
    return scale

# Generate all 12 major scales
# Generate all 12 major scales

# Add an option for generating arpeggios based on a root note
def generate_major_arpeggio(root_note, notes_count):
    # Major arpeggio intervals: root, major third, perfect fifth
    intervals = [0, 4, 7]
    arpeggio = [(root_note + interval, 64, 480) for interval in intervals]
    return arpeggio[:notes_count]

# Add a function to repeat sequences for a given number of repetitions
def repeat_sequences(sequences, repetitions):
    return sequences * repetitions

# Add a function to generate major triads arpeggio
def generate_major_triads_arpeggio(start_note=60, velocity=64, quarter_duration=480):
    """
    Generates an arpeggio through all major triad chords.

    :param start_note: The MIDI note number for the starting note (default is 60 for Middle C).
    :param velocity: The velocity for each note (default is 64).
    :param quarter_duration: Duration of a quarter note in MIDI ticks (default is 480).
    :return: List of tuples representing the arpeggio pattern for all major triads.
    """
    major_triads = []
    
    for i in range(12):  # Iterate over 12 semitones to cover all major triads
        base_note = start_note + i  # Starting note for the current triad
        
        # Append the arpeggio pattern for the current major triad
        major_triads.extend([
            (base_note, velocity, quarter_duration),              # Root
            (base_note + 4, velocity, quarter_duration),          # Major third
            (base_note + 7, velocity, quarter_duration),          # Perfect fifth
            (base_note + 12, velocity, 2 * quarter_duration),     # Octave
            (base_note + 7, velocity, quarter_duration),          # Perfect fifth
            (base_note + 4, velocity, quarter_duration),          # Major third
            (base_note, velocity, 2 * quarter_duration),          # Root
        ])
    
    return major_triads


def generate_circle_of_fifths_arpeggio(start_note, velocity=64, quarter_duration=480):
    arpeggios = []
    for _ in range(12):
        arpeggios.extend([
            (start_note, velocity, quarter_duration),
            (start_note + 4, velocity, quarter_duration),
            (start_note + 4, velocity, quarter_duration),
            (start_note + 4, velocity, quarter_duration),
            (start_note, velocity, quarter_duration),
        ])
        start_note = (start_note - 5) % 12 + 60  # Move down a fourth (up a fifth)
    return arpeggios

def piano_fun(velocity=64, quarter_duration=480):
    # Define the C3, C4, and C5 octaves
    octaves = [48, 60, 72]  # MIDI note numbers for C3, C4, C5
    # Define the circle of fifths sequence
    circle_of_fifths = [60, 67, 74, 65, 72, 79, 70, 77, 62, 69, 76, 71, 78, 63, 68, 75]
    
    # Generate scales and chords based on the circle of fifths
    scales_and_chords = []
    for root_note in circle_of_fifths:
        # Generate a major scale
        scale = generate_major_scale(root_note)
        # Generate a major arpeggio
        arpeggio = generate_major_arpeggio(root_note, 3)
        # Combine scale and arpeggio
        scales_and_chords.extend(scale + arpeggio)
    
    # Create runs by randomly selecting notes from scales
    runs = random.sample(scales_and_chords, k=16)  # Randomly select 16 notes for a run
    
    # Combine octaves with the generated music elements
    music_piece = []
    for note, velocity, ticks in scales_and_chords + runs:
        octave = random.choice(octaves)
        music_piece.append((note + octave - 60, velocity, ticks))  # Adjust note to the selected octave
    
    # Randomize the order of the music piece
    random.shuffle(music_piece)
    
    return music_piece



# Prompt the user for the number of repetitions
repetitions = int(input("Enter the number of repetitions for the sequences: ").strip())


# Generate all 12 major scales and add them to the scale_sequences dictionary
# Generate all 12 major scales and add them to the scale_sequences dictionary
all_scales = {str(i+1): generate_major_scale(root_note) for i, root_note in enumerate(range(60, 72))}
scale_sequences.update(all_scales)

# Add the circle of fifths arpeggio to the scale_sequences dictionary
scale_sequences['circle_of_fifths'] = generate_circle_of_fifths_arpeggio(60)

# Prompt the user to select between scales, arpeggios, AR1, major_triads, or circle_of_fifths
# user_choice = input("Do you want 'scales' (1-12), 'arpeggios' (a), 'AR1' (ar1), 'major_triads' (mt), or 'circle_of_fifths' (cf)? Type your choice: ").strip().lower()


selections = []
# Update the selection logic to handle the new option

valid_options = ['1', '2'] + list(map(str, range(3, 13))) + ['a', 'ar1', 'mt', 'cf', 'pf']



def get_user_input(prompt, valid_options=None, default=None):
    while True:
        user_input = input(prompt).strip().lower()
        if valid_options is None or user_input in valid_options:
            return user_input
        else:
            print(f"Invalid input. Please enter one of the following: {', '.join(valid_options)}")
            if default is not None:
                return default


# Use the new get_user_input function
user_choice = input("Do you want 'scales' (1-12), 'arpeggios' (a), 'AR1' (ar1), 'major_triads' (mt), 'circle_of_fifths' (cf), or 'piano_fun' (pf)? Type your choice: ").strip().lower()

valid_options.append('pf')

if user_choice in ['1', '2'] + list(map(str, range(3, 13))):  # Add more numbers if needed
    selections = [user_choice]
elif user_choice in ['a', 'arpeggios']:
    user_choice = 'arpeggios' 
    # Prompt user for which chords major A-G
    chord_root_note = get_user_input("Enter the root note for the major chord (A-G): ", valid_options=['A', 'B', 'C', 'D', 'E', 'F', 'G'])
    # Convert note to MIDI number (assuming octave 4 for simplicity)
    note_to_midi = {'C': 60, 'D': 62, 'E': 64, 'F': 65, 'G': 67, 'A': 69, 'B': 71}
    root_note_midi = note_to_midi[chord_root_note]  # Default to C if invalid note removed
    # Prompt user for how many notes in each chord to use
    notes_count = int(get_user_input("How many notes in each chord to use (1-3): ", valid_options=['1', '2', '3']))
    # Generate arpeggio
    selections = ['arpeggio']
    scale_sequences['arpeggio'] = generate_major_arpeggio(root_note_midi, notes_count)
elif user_choice == 'ar1':
    selections = ['AR1']
elif user_choice == 'mt':
    selections = ['major_triads']
elif user_choice == 'cf':
    selections = ['circle_of_fifths']
elif user_choice == 'pf':  # Add the 'piano_fun' option
    selections = ['piano_fun']
    scale_sequences['piano_fun'] = piano_fun()
else:
    print("Invalid choice. Please type a valid option.")
    exit()

# Update the creation of the new sequence to include repetitions
new_sequence = []

# Before the loop where you append messages to the track, add the following:
mid = MidiFile()  # Create a new MIDI file
track = MidiTrack()  # Create a new MIDI track
mid.tracks.append(track)  # Add the track to the MIDI file

for selection in selections:
    repeated_sequence = repeat_sequences(scale_sequences[selection], repetitions)
    new_sequence.extend(repeated_sequence)

# Play the new sequence
for note, velocity, ticks in new_sequence:
    track.append(Message('note_on', note=note, velocity=velocity, time=0))
    track.append(Message('note_off', note=note, velocity=velocity, time=ticks))

# Count the number of notes in the new sequence
note_count = len(new_sequence)

# Prompt the user for a custom file name
custom_name = input("Enter a custom name for the MIDI file: ")

# Save the MIDI file with the custom name and the number of notes in the filename
filename = f'{custom_name}_{user_choice}_{note_count}_notes.mid'
mid.save(filename)

print(f"File saved as '{filename}' in the current directory.")