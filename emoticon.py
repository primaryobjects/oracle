from lib.util import execute
from lib.grover import grover
from lib.oracles.entangle import oracle
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister

#
# Superimposed Emotions
#
# Generates an emoticon from two ASCII binary strings that contain nearly identical bits except for a few.
# The differing bits get applied entanglement, resulting in a random selection of either emoticon from the quantum circuit.
# The final output simulataneously represents both emoticons. Measuring the output collapses the state, resulting in a single emotion to display.
#
# Motivated by https://medium.com/qiskit/making-a-quantum-computer-smile-cee86a6fc1de and https://github.com/quantumjim/quantum_emoticon/blob/master/quantum_emoticon.ipynb
# See also the IBM Quantum Composer version at https://quantum-computing.ibm.com/composer/files/d363d10d96ff5f1b9000b64c56a9856a3fbe01a5dd0bb91288a12a47c22a76a8
#
emoticons = [
    ';)', # 00111011 00101001
    '8)'  # 00111000 00101001
          #       ^^----- all bits are the same, except for these two.
]

def decode_binary_string(s):
    """
    Returns an ASCII string for a binary bit string (1 byte [8 bits] per character).
    """
    #n = int(s, 2)
    #return n.to_bytes((n.bit_length() + 7) // 8, 'big').decode()
    return ''.join(chr(int(s[i*8:i*8+8],2)) for i in range(len(s)//8))

def main():
    """
    Return a random emoticon from ;) or 8) by using entangled qubits and bit strings to represent ASCII characters.
    """
    emoticon1 = ';)'
    emoticon2 = '8)'

    # Convert ascii to a binary string.
    b1 = ''.join(format(ord(i), '08b') for i in emoticon1)
    b2 = ''.join(format(ord(i), '08b') for i in emoticon2)

    # Number of qubits, 1 qubit for each bit.
    n = len(b1)

    # Create a quantum circuit.
    var = QuantumRegister(n, 'var')
    cr = ClassicalRegister(n, 'c')
    qc = QuantumCircuit(var, cr)

    # Append the oracle, which encodes the binary values and applies entanglement accordingly.
    qc.append(oracle(b1, b2, [[8, 9]]), range(n))

    # Measure all qubits to force a single result out of superposition.
    qc.measure(var, cr)

    print(qc.draw())

    # Run the circuit several times to show the difference in superposition state.
    results = []
    for i in range(1000):
        # Execute the quantum circuit.
        result = execute(qc)

        # Get the resulting hit counts.
        counts = result.get_counts()

        if i == 0:
            print(counts)

        # Find the most frequent hit count.
        key = max(counts, key=counts.get)

        # Decode the bits into ASCII characters (8 bits [1 byte] per character).
        result = decode_binary_string(key)
        results += result

        # Print the output, random result of emoticon1 or emotion2!
        if i > 0 and i % 80 == 0:
            print(''.join(results))
            results.clear()

main()