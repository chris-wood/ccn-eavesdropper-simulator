from runner import *
from network import *


# Ts = range(10, 100000, 1000)
Ts = range(10, 10000, 1000)
Ns = range(10, 1000, 100)
# Ns = range(10, 100, 10)

S = 16

processes = []

for T in Ts:
    for N in Ns:
        fout = "ideal_size_%d_%d.txt" % (T, N)
        processes.append(create_simulation(T, N, S, 1, create_path, lambda items : ZipfDistribution(1.3, items), lambda items : ZipfDistribution(1.3, items), 1.0, 0.0, fout))

for p in processes:
    p.start()

for p in processes:
    p.join()
\
