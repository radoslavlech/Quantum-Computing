from qiskit import BasicAer
from qiskit import execute
from qiskit import QuantumRegister
from qiskit import ClassicalRegister
from qiskit import QuantumCircuit
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt
from functions import *
from fractions import Fraction

#n = int(np.floor(np.log2(N)))+1
m = 4  #number of qubits used in the QFT register
a = 2
N = 15

q = QuantumRegister(5, 'q')
c = ClassicalRegister(m, 'c')

qc = QuantumCircuit(q, c)
circuit_aperiod15(qc,q,c,a)


fig = plt.figure(qc.draw('mpl'))


backend = BasicAer.get_backend('qasm_simulator')
sim_job = execute([qc], backend)
sim_result = sim_job.result()
sim_data = sim_result.get_counts(qc)
print(sim_data)

fig2 = plt.figure(plot_histogram(sim_data))



plt.show()



#POSTPROCESSING
# Define Q as 2 to the power of the number of qubits used in the QFT
Q = 2**m


# Find the period r using the continued fraction expansion
potential_rs = set()

for measured_value in sim_data:
    measured_value_int = int(measured_value, 2)
    for denominator in range(2, Q):
        fraction = Fraction(measured_value_int, Q).limit_denominator(denominator)
        if fraction.denominator not in potential_rs and abs(fraction - Fraction(measured_value_int, Q)) < 1/Q:
            potential_rs.add(fraction.denominator)



# Attempt to find factors for each potential r
factors = set()

for r in potential_rs:
    if r % 2 == 0 and a**(r//2) % N != N - 1:  # additional check to ensure a^(r/2) is not congruent to -1 mod N
        possible_factor_1 = GCD(a**(r//2) - 1, N)
        possible_factor_2 = GCD(a**(r//2) + 1, N)
        if 1 < possible_factor_1 < N:
            factors.add(possible_factor_1)
        if 1 < possible_factor_2 < N:
            factors.add(possible_factor_2)


# Output the non-trivial factors
if factors:
    print(f"The non-trivial factors of {N} are: {factors}")
else:
    print(f"No non-trivial factors found. The period might not be correct or 'a' might not be a good choice.")
