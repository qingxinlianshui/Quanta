"""
This is a example of the realization of Quantum Teleportation with QISKIT, created on 14th November, 2019.
"""
# Import numpy for the usage of np.pi
import numpy as np

from collections import Counter

import time,sys

# Import brief QISKIT modules
from qiskit import (QuantumCircuit, QuantumRegister, ClassicalRegister, execute, Aer, IBMQ, providers)

# Import basic plotting tools
from qiskit.visualization import plot_histogram

# Define the calculation function
def calculation():

    # Create registers 
    q = QuantumRegister(3)
    c0 = ClassicalRegister(1)
    c1 = ClassicalRegister(1)
    c2 = ClassicalRegister(1)
    
# Create quantum circuit
    circ = QuantumCircuit(q,c0,c1,c2, name = 'circ')

# Quantum state to be teleported
 #   circ.u1(np.pi/4, q[0])
    circ.u3(np.pi/4, np.pi/4, np.pi/4, q[0])
    circ.h(q[1])
    circ.cx(q[1],q[2])
 #   circ.barrier(q)
    circ.cx(q[0],q[1])
    circ.h(q[0])
    circ.barrier(q)
    circ.measure(q[0], c0[0])
    circ.measure(q[1], c1[0])

    circ.z(q[2]).c_if(c0,1)
    circ.x(q[2]).c_if(c1,1)
    circ.measure(q[2], c2[0])

    backend = Aer.get_backend('qasm_simulator') # The Aer's qasm_simulator
 #   IBMQ.load_account()
 #   backend = providers.ibmq.least_busy(IBMQ.backends(simulator=False))
 #   print("The least busy device is chosen:",backend.name())
 #   job = execute(circ, backend,shots = 1024)

    job = execute(circ, backend = backend, shots = 1024, max_credits= 3) # Execute the circuit on the qasm_simulator and set 1024 shots
    result = job.result()
    counts = result.get_counts(circ)
    print("Counts:",counts)

# Figure out that has to merge two dicts
    dic = {'0 0 0':0, '0 0 1':0, '0 1 0':0, '0 1 1':0, '1 0 0':0, '1 0 1':0, '1 1 1':0}
    A= Counter(dic)
    B = Counter(counts)
    data = A+B

    send = {}
    send['00'] = data['0 0 0']+ data['1 0 0']
    send['10'] = data['0 1 0']+ data['1 1 0']
    send['01'] = data['0 0 1']+ data['1 0 1']
    send['11'] = data['0 1 1']+ data['1 1 1']
    plot_histogram(send)

    receiver = {}
    receiver['0'] = data['0 0 0']+ data['0 1 0']+ data['0 0 1']+ data['0 1 1']
    receiver['0'] = data['1 0 0']+ data['1 1 0']+ data['1 0 1']+ data['1 1 1']
    plot_histogram(receiver)

if __name__ == '__main__':
    start_time = time.time()
    calculation()
    print("Calculation time:", (time.time()-start_time),"s")
