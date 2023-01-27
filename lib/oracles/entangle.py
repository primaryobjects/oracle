from qiskit import QuantumCircuit

def oracle(b1, b2, entanglements):
    '''
    Takes two bit strings (b1 and b2) and entangles the qubits at indices entanglements[] using CNOT.
    Returns a quantum circuit that represents the state of both bit strings simultaneously.
    Measuring the result will force an outcome of b1 or b2.
    Parameters:
    b1, b2: bit strings (for example, 16 bit ASCII character)
    entanglements: list of pairs of indices to entangle qubits. For example: [ [9, 8], [control, target], ... ]
    '''

    b1 = b1[::-1]
    b2 = b2[::-1]

    # Number of qubits will be 1 qubit for each bit.
    n = len(b1)

    # We use a circuit of size n.
    qc = QuantumCircuit(n)

    # Flip all qubits that have a 1 in the bit string.
    for i in range(n):
        if b1[i] == '1' and b2[i] == '1':
            qc.x(i)

    # Entangle qubits.
    for entanglement in entanglements:
        control = entanglement[0]
        target = entanglement[1]

        # Place control qubit in superposition.
        qc.h(control)
        
        # Entangle target qubit to control, spreading superposition and state.
        qc.cx(control, target)

    print(qc.draw())

    # Convert the oracle to a gate.
    gate = qc.to_gate()
    gate.name = "oracle"

    return gate
