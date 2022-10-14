from typing import List, Dict
import pyfiglet
from random import choices
import time

"""
Just some static configuration settings
"""
BITS_PER_NOTE = 4
NOTES = ['C# 3.0', 'D# 3.0', 'F 3.0', 'F# 3.0', 'G# 3.0', 'A# 4.0', 'B 4.0', 'C# 4.0', 'D# 4.0', 'F 4.0', 'F# 4.0', 'G# 4.0', 'A# 5.0', 'B 5.0', 'C# 5.0']


def generate_genome(length: int) -> List[int]:
    """
    Create a genome! (just a random choices call)
    :param length: the length of the genome
    :return: the generated genome
    """
    return choices([0, 1], k=length)


def int_from_bits(bits: List[int]) -> int:
    """
    Does exactly what it says
    :param bits: the bits
    :return:  the int
    """
    return int(sum([bit*pow(2, index) for index, bit in enumerate(bits)]))


def genome_to_melody(genome: List[int], num_bars: int, num_notes: int, num_steps: int) -> Dict[str, list]:
    """
    Converts a genome to melody
    :param genome:  the genome
    :param num_bars:    the number of bars
    :param num_notes:   the number of notes
    :param num_steps:   the number of steps
    :return:            the melody
    """
    # Create genomes and stuff
    notes = [genome[i * BITS_PER_NOTE:i * BITS_PER_NOTE + BITS_PER_NOTE] for i in range(num_bars * num_notes)]
    note_length = 4 / float(num_notes)
    melody = {"notes": [], "velocity": [], "beat": []}

    for note in notes:
        integer = int_from_bits(note)
        integer = int(integer % pow(2, BITS_PER_NOTE - 1))

        if integer >= pow(2, BITS_PER_NOTE - 1):
            melody["notes"] += [0]
            melody["velocity"] += [0]
            melody["beat"] += [note_length]
        else:
            if len(melody["notes"]) > 0 and melody["notes"][-1] == integer:
                melody["beat"][-1] += note_length
            else:
                melody["notes"] += [integer]
                melody["velocity"] += [127]
                melody["beat"] += [note_length]

    steps = []
    for step in range(num_steps):
        steps.append([NOTES[(note+step*2) % len(NOTES)] for note in melody["notes"]])

    melody["notes"] = steps
    return melody


def display_genome(genome: List[int], num_bars: int, num_notes: int, num_steps: int):
    """
    Creates and displays a genome
    :param genome:  the genome
    :param num_bars: the number of bars
    :param num_notes: the number of bars
    :param num_steps: the number of steps
    """
    melody = genome_to_melody(genome, num_bars, num_notes, num_steps)

    print(len(melody['notes'][0]))
    for i in range(len(melody['notes'][0])):
        note = melody['notes'][0][i]
        note = pyfiglet.figlet_format(note, font='big')
        print(note)
        time.sleep(melody['beat'][i])
        print("\n\n\n")


def main(num_bars=20, num_notes=4, num_steps=1):
    genome = generate_genome(num_bars * num_notes * BITS_PER_NOTE)
    display_genome(genome, num_bars, num_notes, num_steps)


if __name__ == '__main__':
    main()
