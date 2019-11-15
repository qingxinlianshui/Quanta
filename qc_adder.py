"""
The Quantum ripple-carry adder based on "A new quantum ripple-carry addition circuit" (Cuccaro et al. 2018)
"""
import numpy as np
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit import(QuantumCircuit, execute, Aer,IBMQ)
from qiskit.visualization import plot_histogram

sub_maj = QuantumRegister(3)
sub_uma = QuantumRegister(3)

maj = QuantumCircuit(sub_maj, name = 'maj')
maj.cx(sub_maj[2], sub_maj[1])
maj.cx(sub_maj[2], sub_maj[0])
maj.ccx(sub_maj[0], sub_maj[1], sub_maj[2])
sub_maj_inst = maj.to_instruction()


uma = QuantumCircuit(sub_uma, name = 'uma')
uma.ccx(sub_uma[0],sub_uma[1],sub_uma[2])
uma.cx(sub_uma[2], sub_uma[0])
uma.cx(sub_uma[0], sub_uma[1])
sub_uma_inst = uma.to_instruction()


cin = QuantumRegister(1,'cin')
qa = QuantumRegister(4,'a')
qb = QuantumRegister(4,'b')
cout = QuantumRegister(1, 'cout')
ans = ClassicalRegister(5, 'ans')

circ = QuantumCircuit(cin, qa, qb, cout, ans)
circ.x(qa[0])
circ.x(qb)


circ.append(maj, [cin[0], qb[0], qa[0]])
circ.append(maj, [qa[0], qb[1], qa[1]])
circ.append(maj, [qa[1], qb[2], qa[2]])
circ.append(maj, [qa[2], qb[3], qa[3]])

circ.cx(qa[3], cout[0])

circ.append(uma, [qa[2], qb[3], qa[3]])
circ.append(uma, [qa[1], qb[2], qa[2]])
circ.append(uma, [qa[0], qb[1], qa[1]])
circ.append(uma, [cin[0], qb[0], qa[0]])

circ.measure(qb[0],ans[0])
circ.measure(qb[1],ans[1])
circ.measure(qb[2],ans[2])
circ.measure(qb[3],ans[3])
circ.measure(cout[0],ans[4])

backend_sim = Aer.get_backend('qasm_simulator') # The Aer's qasm_simulator
job_sim = execute(circ, backend_sim, shots = 1024) # Execute the circuit on the qasm_simulator and set 1024 shots
result_sim = job_sim.result()
counts = result_sim.get_counts(circ)
print(counts)

plot_histogram(counts)
