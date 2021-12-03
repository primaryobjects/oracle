from lib.util import execute
from lib.grover import grover
from lib.oracles.odd import oracle

def main():
    # Find all odd numbers in a given range.
    execute.provider = None

    # Generate the quantum circuit.
    qc = grover(oracle, None, 3)
    print(qc.draw())

    # Execute the quantum circuit.
    result = execute(qc)

    # Get the resulting hit counts.
    counts = result.get_counts()
    print(counts)

main()