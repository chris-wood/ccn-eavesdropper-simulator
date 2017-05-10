from runner import *
from network import *

Ts = [10000]
Ns = [50, 100]
Ps = [1, 2, 4]
Cs = [25]

S = 16

adv_p = 0.1

processes = []

for T in Ts:
    for N in Ns:
        for P in Ps:
            for C in Cs:
                fout = "split_lattice_%d_%d_%d_%d_%f.txt" % (T, N, P, C, adv_p)
                processes.append(create_split_simulation(T, N, S, P, create_lattice_network, lambda items : ZipfDistribution(1.3, items), lambda items : ZipfDistribution(1.3, items), adv_p, 0.0, fout, C))

for p in processes:
    p.start()

for p in processes:
    p.join()
