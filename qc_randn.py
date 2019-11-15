"""
This is an quantum program used for generating random number. Created on November 11, 2019
"""
import numpy as np
from qiskit import(QuantumCircuit, execute, Aer,IBMQ) # load modules for quantum computing
import time,sys
from qiskit.tools.monitor import job_monitor

def qc(n):
    # Create Quantum Circuit
    circ = QuantumCircuit(n,n) # Create a Quantum Circuit of n qubits
    circ.h(range(n))
    for i in range(n):
        circ.measure(i,i)


    # Assign the simulator
    backend_sim = Aer.get_backend('qasm_simulator') # The Aer's qasm_simulator
    job_sim = execute(circ, backend_sim, shots = 1024) # Execute the circuit on the qasm_simulator and set 1024 shots
    result_sim = job_sim.result()
    counts = result_sim.get_counts(circ)
    print(counts)
"""
Implement real Quantum Computing device
"""
    provider = IBMQ.get_provider(group = 'open')
    backend = provider.get_backend('ibmqx4')
    job = execute(circ, backend = backend, shots = 1024)
    job_monitor(job)
    result = job.result()
    counts_real = result.get_counts(circ)
    print(counts_real)

    bits = ""
    for x in counts.values():
        if x > shots/(2**n):
            bits += "1"
        else:
            bits += "0"
    return int(bits, 2)

if __name__ == '__main__':
    start_time = time.time()
    numbers = []
    size = 10
    qubits = 3 # bits = 2**qubits
    shots = 1024
    for i in range(size):
        n = qc(qubits)
        numbers.append(n)
    print("list=" + str(numbers))
    print("Calculation time:", (time.time()-start_time),"s")
