from qiskit import QuantumCircuit
from qiskit.circuit.library.standard_gates.z import ZGate

def oracle(logic, n):
    '''
    Returns a quantum circuit that recognizes even numbers. We do this by checking if qubit 0 equals 0 (even).
    Upon starting, all qubits are assumed to have a value of 1. We only need to consider qubit 0, the other qubits may be ignored.
    Parameters:
    logic: not used (should be None).
    n: the number of qubits in the circuit.
    '''

    # We use a circuit of size n+1 to include an output qubit.
    qc = QuantumCircuit(n+1)

    # Flip the first qubit to 0, since we want to obtain that value.
    qc.x(0)

    # Apply a controlled Z-gate from qubit 0 to each of the other qubits. When qubit 0 is 0, the others are flipped, setting the phase.
    qc.append(ZGate().control(1), [0,range(1,n+1)])
    # qc.append(ZGate().control(1), [0,1])
    # qc.append(ZGate().control(1), [0,2])
    # qc.append(ZGate().control(1), [0,3])

    # Undo the flip of the first qubit.
    qc.x(0)

    print(qc.draw())

    # Convert the oracle to a gate.
    gate = qc.to_gate()
    gate.name = "oracle"

    return gate
