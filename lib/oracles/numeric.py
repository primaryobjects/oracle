from qiskit import QuantumCircuit
from qiskit.circuit.library.standard_gates.z import ZGate

def oracle(i, n):
    '''
    Returns a quantum circuit that recognizes a single number i.
    Upon starting, all qubits are assumed to have a value of 1.
    Parameters:
    i: the target value to be recognized, an integer between 0 and 2^n-1.
    n: the number of qubits in the circuit.
    '''

    # We use a circuit of size n+1 to include an output qubit.
    qc = QuantumCircuit(n+1)

    # Convert i to a binary string.
    bin_str = bin(i)[2:]

    # Pad the binary string with zeros to the length of the qubits.
    bin_str = bin_str.zfill(n)

    print('Encoding ' + bin_str)

    # Reverse the bits since qiskit represents the qubits from right to left.
    bin_str = bin_str[::-1]

    # Flip each qubit to zero to match the bits in the target number i.
    for j in range(len(bin_str)):
        if bin_str[j] == '0':
            qc.x(j)

    # Apply a controlled Z-gate on all qubits, setting the phase.
    qc.append(ZGate().control(n), range(n+1))

    # Undo each inverted qubit.
    for j in range(len(bin_str)):
        if bin_str[j] == '0':
            qc.x(j)

    print(qc.draw())

    # Convert the oracle to a gate.
    gate = qc.to_gate()
    gate.name = "oracle"

    return gate
