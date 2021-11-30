import random
from math import ceil, log
from lib.util import execute
from lib.grover import grover
from lib.oracles.numeric import oracle

predictions = [
    'It is certain.',
    'It is decidedly so.',
    'Without a doubt.',
    'Yes definitely.',
    'You may rely on it.',
    'As I see it, yes.',
    'Most likely.',
    'Outlook good.',
    'Yes.',
    'Signs point to yes.',
    'Reply hazy, try again.',
    'Ask again later.',
    'Better not tell you now.',
    'Cannot predict now.',
    'Concentrate and ask again.',
    'Don''t count on it.',
    'My reply is no.',
    'My sources say no.',
    'Outlook not so good.',
    'Very doubtful.'
]

def main():
    """
    Return a random prediction from a dictionary, selecting the index using Grover's search.
    Example:
    Please ask me a yes/no question and I will predict your future [PRESS ANY KEY] ...

    Selected random index 4
    Encoding 00100

    {'01000': 27, '01111': 27, '01110': 26, '11010': 31, '11001': 32, '00010': 27, '11101': 25, '10100': 27, '11100': 31, '11110': 24, '00111': 35, '01100': 31, '01010': 36, '10001': 30, '00011': 32, '00100': 135, '10011': 23, '00110': 25, '11111': 27, '10010': 23, '10110': 34, '10111': 34, '11000': 34, '00101': 36, '01001': 31, '10000': 19, '10101': 29, '00000': 26, '01011': 28, '00001': 23, '01101': 26, '11011': 30}
    Result: 4 (00100)

    You may rely on it.
    """

    execute.provider = None

    input('Please ask me a yes/no question and I will predict your future [PRESS ANY KEY] ...')

    # Determine the number of qubits required.
    n = ceil(log(len(predictions), 2))

    # Select a random prediction.
    r = random.choice(range(len(predictions)))

    print()
    print('Selected random index ' + str(r))

    # Generate the quantum circuit.
    qc = grover(oracle, r, n)
    print(qc.draw())

    # Execute the quantum circuit.
    result = execute(qc)

    # Get the resulting hit counts.
    counts = result.get_counts()
    print(counts)

    # Find the most frequent hit count.
    key = max(counts, key=counts.get)

    # Since the quantum computer returns a binary string (one bit for each qubit), we need to convert it to an integer.
    index = int(key, 2)

    print()
    print('Result: ' + str(index) + ' (' + key + ')')

    # Print the resulting prediction from the quantum circuit.
    print()
    print(predictions[index])

main()