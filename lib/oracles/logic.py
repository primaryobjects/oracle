from qiskit import QuantumCircuit
from qiskit.circuit.classicalfunction.classicalfunction import ClassicalFunction

def oracle(logic, n):
    '''
    Returns a quantum circuit that implementes the logic for n qubits.
    Parameters:
    logic: a Python function using the format below.
            def oracle_func(x1: Int1, x2: Int1, x3: Int1) -> Int1:\n  return (x1 and not x2 and not x3)
    n: the number of qubits in the circuit.
    '''

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
