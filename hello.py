import random
from math import ceil, floor, log
from lib.util import execute, generate
from lib.grover import grover
from lib.oracles.logic import oracle

def init(target, n):
    # Initialize an array of random letters, including the target ones in the string.
    arr = generate(n)

    # Store used indices so that we don't overwrite target letters.
    indices = [-1]

    # Select random indices for the target letters.
    for i in range(len(target)):
        index = -1

        # Select a random index until we find one that hasn't been used.
        while index in indices:
            index = random.randint(0, n - 1)

        # Set the target letter at the selected index.
        arr[index] = target[i]

        # Add the index to the list of used indices.
        indices.append(index)
    return arr

def logic(arr, target, n):
    # Finds the indices within arr for each position of target letter and returns a Python function as a string to be used in an oracle.
    prog = '''def oracle_func(_PARAMS_) -> Int1:
            return _CLAUSE_'''

    # Insert the parameters for the function, based upon the number of qubits needed for target.
    qubits = floor(log(n, 2))
    params = ''
    for i in range(qubits):
        # x1: Int1, x2: Int1, x3: Int1
        params += 'x' + str(i + 1) + ': Int1, '

    # Remove the trailing comma.
    params = params[:-2]
    prog = prog.replace('_PARAMS_', params)

    # Insert the clauses for the function, based upon the bit location(s) for the target letter.
    # (not x1 and not x2 and not x3) or (x1 and x2 and not x3)
    clauses = ''
    # Find the next index of the target letter.
    index = arr.index(target, 0)
    while index != -1:
        # Convert the index to a binary string.
        bin_str = bin(index)[2:]

        # Pad the binary string with zeros to the length of the qubits.
        bin_str = bin_str.zfill(qubits)

        # Generate the logical string for the clause.
        clause = ''
        for j in range(len(bin_str)-1, -1, -1):
            if bin_str[j] == '0':
                clause += 'not '
            clause += 'x' + str(len(bin_str) - j) + ' and '

        # Trim trailing 'and ' from the clause.
        clause = clause[:-5]

        # Add parentheses to the clause.
        clause = '(' + clause + ')'

        # Insert the clause into the clauses.
        clauses += clause + ' or '

        # Find the next index matching the letter (if any more exist).
        try:
            index = arr.index(target, index + 1)
        except ValueError:
            # No more letters found.
            index = -1

    # Trim trailing 'or ' from the clauses.
    clauses = clauses[:-4]
    prog = prog.replace('_CLAUSE_', clauses)

    return prog

def main(phrase):
    execute.provider = None

    # Calculate the number of qubits needed to represent the number of letters in the target.
    qubits = ceil(log(len(phrase), 2))

    bits = 2 ** qubits
    arr = init(phrase, bits)

    print(str(qubits) + ' qubits, ' + str(bits) + ' possibilites')
    print('Using random letters:')
    print(arr)

    # Use the oracle to find the indices of the target letters.
    indices = []
    for letter in phrase:
        print("Finding letter '" + letter + "'")

        # Generate a logical function for the oracle.
        prog = logic(arr, letter, bits)

        # Generate the quantum circuit.
        qc = grover(oracle, prog, qubits)
        #print(qc.draw())

        # Execute the quantum circuit.
        result = execute(qc)

        # Get the resulting hit counts.
        counts = result.get_counts()
        print(counts)

        # Find the most frequent hit count.
        key = max(counts, key=counts.get)

        # Since the quantum computer returns a binary string (one bit for each qubit), we need to convert it to an integer.
        index = int(key, 2)

        # Print the resulting letter selected by the quantum circuit.
        print(arr[index])

        indices.append({'binary': key, 'index': index, 'letter': letter})

    print('Random letters:')
    print(arr)

    print('Final result from the quantum circuit:')
    for i in range(len(indices)):
        letter = arr[indices[i]['index']]
        index = indices[i]['index']
        binary = indices[i]['binary']

        print(letter + ' (at index ' + str(index) + ' [' + binary + '])')

main('hello')
