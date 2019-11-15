"""
This is a realization of half adder with qiskit toolkit, created on 14th November, 2019
"""
import numpy as np
from qiskit import(QuantumCircuit, execute, Aer,IBMQ) # load modules for quantum computing
import time,sys
from qiskit.tools.monitor import job_monitor
from qiskit.visualization import plot_histogram

circ = QuantumCircuit(4,2) # Four qubits to perform 1+1
circ.x(0)
circ.x(1)

circ.barrier(range(4))

circ.cx(1,2)
circ.cx(0,2)
circ.ccx(0,1,3)

circ.barrier(range(4))

circ.measure(2,0)
circ.measure(3,1)

   # Assign the simulator
backend_sim = Aer.get_backend('qasm_simulator') # The Aer's qasm_simulator
job_sim = execute(circ, backend_sim, shots = 1024) # Execute the circuit on the qasm_simulator and set 1024 shots
result_sim = job_sim.result()
counts = result_sim.get_counts(circ)
print(counts)
plot_histogram(counts)
