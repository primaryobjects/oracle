import ast
import random
import string
import time
from configparser import RawConfigParser
from qiskit import qiskit, Aer, IBMQ

def generate(n):
    # Generate an array of random letters.
    letters = []
    for i in range(n):
        letters.append(random.choice(string.ascii_letters))
    return letters

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