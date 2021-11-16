from qiskit import QuantumCircuit
from qiskit.circuit.classicalfunction.classicalfunction import ClassicalFunction

def oracle(logic, n):
    # Returns a quantum circuit that implementes the logic for n qubits.

    # Convert the logic to a quantum circuit.
    formula = ClassicalFunction(logic)
    fc = formula.synth()

    # Convert the quantum circuit to a quantum program.
    qc = QuantumCircuit(n+1)
    qc.compose(fc, inplace=True)

    print(qc.draw())

    # Convert the oracle to a gate.
    gate = qc.to_gate()
    gate.name = "oracle"

    return gate
