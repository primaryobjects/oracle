from qiskit import QuantumCircuit
from qiskit.circuit.classicalregister import ClassicalRegister
from qiskit.circuit.quantumregister import QuantumRegister

def diffuser(n):
    qc = QuantumCircuit(n)

    # Apply transformation |s> -> |00..0> (H-gates)
    qc.h(range(n))

    # Apply transformation |00..0> -> |11..1> (X-gates)
    qc.x(range(n))

    # Do multi-controlled-Z gate
    qc.h(n-1)
    qc.mct(list(range(n-1)), n-1)  # multi-controlled-toffoli
    qc.h(n-1)

    # Apply transformation |11..1> -> |00..0>
    for qubit in range(n):
        qc.x(qubit)

    # Apply transformation |00..0> -> |s>
    qc.h(range(n))

    # We will return the diffuser as a gate
    gate = qc.to_gate()
    gate.name = "diffuser"

    return gate

def grover(oracle, logic, n):
    # The circuit is a Grover's search for the all-ones state.
    var = QuantumRegister(n, 'var')
    out = QuantumRegister(1, 'out')
    cr = ClassicalRegister(n, 'c')
    qc = QuantumCircuit(var, out, cr)

    # Initialize the output qubit to a phase-flip.
    qc.x(n)
    qc.h(n)

    # Apply the Hadamard gate to every qubit.
    qc.h(var)
    qc.barrier()

    # Apply the oracle to every qubit.
    qc.append(oracle(logic, n), range(n+1))
    qc.barrier()

    # Apply the diffuser to every qubit.
    qc.append(diffuser(n), range(n))
    qc.barrier()

    # Undo the output qubit phase-flip.
    qc.h(n)
    qc.x(n)

    qc.measure(var, cr)

    return qc