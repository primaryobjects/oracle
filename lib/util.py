import ast
import random
import string
import time
from math import ceil, log
from configparser import RawConfigParser
from qiskit import qiskit, Aer, IBMQ, QuantumCircuit

def random_letters(n):
    # Generate an array of random letters.
    letters = []
    for i in range(n):
        letters.append(random.choice(string.ascii_letters))
    return letters

def random_number(minimum, maximum):
    # Uses a quantum circuit to generate a random number from minimum (inclusive) to maximum (exclusive).
    # Determine the number of qubits required.
    n = num_qubits(maximum-1)

    # Create a quantum circuit with enough qubits for the max value.
    qc = QuantumCircuit(n)

    # Place all qubits into superposition.
    qc.h(range(n))

    # Measure the result.
    qc.measure_all()

    # Continue executing the circuit until we obtain a value within range.
    r = -1
    count = 0
    max_count = 10
    while (r < minimum or r >= maximum) and count < max_count:
        # Execute the circuit.
        result = execute(qc)

        # Get the resulting hit counts.
        counts = result.get_counts()

        # Find the most frequent hit count.
        key = max(counts, key=counts.get)

        # Since the quantum computer returns a binary string (one bit for each qubit), we need to convert it to an integer.
        r = int(key, 2)

        # Increment the count before we break.
        count = count + 1

    return r

def num_qubits(i):
    # Returns the number of qubits needed to represent the value i.
    return ceil(log(i, 2))

def execute(qc):
    # Setup the API key for the real quantum computer.
    parser = RawConfigParser()
    parser.read('config/config.ini')

    # Read configuration values.
    proxies = ast.literal_eval(parser.get('IBM', 'proxies')) if parser.has_option('IBM', 'proxies') else None
    verify = (True if parser.get('IBM', 'verify') == 'True' else False) if parser.has_option('IBM', 'verify') else True
    token = parser.get('IBM', 'key')

    is_sim = token == 'YOUR_API_KEY'
    if not is_sim:
        execute.provider = execute.provider or IBMQ.enable_account(token = token, proxies = proxies, verify = verify)
        backend = execute.provider.backends(simulator=False)[1]
    else:
        backend = Aer.get_backend('aer_simulator')

    if not is_sim:
        print("Running on", backend.name())

    start = time.time()
    job = qiskit.execute(qc, backend)
    result = job.result()
    stop = time.time()

    if not is_sim:
        print("Request completed in " + str(round((stop - start) / 60, 2)) + "m " + str(round((stop - start) % 60, 2)) + "s")

    return result